import os
import sys

from setuptools.command.build_ext import build_ext as setuptools_build_ext
from setuptools._distutils.extension import Extension

from .compiler import ClangWASICompiler
from .core import download_sdk, CPYTHON_INCLUDE_DIR, WASI_SDK, WASI_LIB_DIR


class build_ext(setuptools_build_ext):
    def run(self):
        if not WASI_SDK.exists():
            download_sdk()

        ext = ".cp" + "".join(map(str, sys.version_info[:2]))
        ext += "-wasm32_wasip1_threads.wasm"
        os.environ["SETUPTOOLS_EXT_SUFFIX"] = ext

        # override default dirs with our own
        self.include_dirs.insert(0, CPYTHON_INCLUDE_DIR)
        self.library_dirs = [str(WASI_LIB_DIR)]
        self.libraries.insert(0, "c")

        # adapted from setuptools.command.build_ext.build_ext.run
        old_inplace, self.inplace = self.inplace, 0
        self._run()
        self.inplace = old_inplace
        if old_inplace:
            self.copy_extensions_to_source()

    def _run(self):
        # adapted from distutils.command.build_ext.build_ext.run
        if not self.extensions:
            return

        if self.distribution.has_c_libraries():
            build_clib = self.get_finalized_command("build_clib")
            self.libraries.extend(build_clib.get_library_names() or [])
            self.library_dirs.append(build_clib.build_clib)

        # use clang compiler
        self.compiler = ClangWASICompiler(None, self.dry_run, self.force)

        if self.include_dirs is not None:
            self.compiler.set_include_dirs(self.include_dirs)
        if self.define is not None:
            for name, value in self.define:
                self.compiler.define_macro(name, value)
        if self.undef is not None:
            for macro in self.undef:
                self.compiler.undefine_macro(macro)
        if self.libraries is not None:
            self.compiler.set_libraries(self.libraries)
        if self.library_dirs is not None:
            self.compiler.set_library_dirs(self.library_dirs)
        if self.rpath is not None:
            self.compiler.set_runtime_library_dirs(self.rpath)
        if self.link_objects is not None:
            self.compiler.set_link_objects(self.link_objects)

        self.build_extensions()

    def get_libraries(self, ext):
        # remove libpython
        return super().get_libraries(ext)[:-1]
