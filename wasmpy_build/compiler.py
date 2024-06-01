from setuptools._distutils.unixccompiler import UnixCCompiler
from setuptools.errors import CompileError, ExecError

from .core import WASI_SDK


class ClangWASICompiler(UnixCCompiler):
    compiler_type = "clang-wasi"
    shared_lib_extension = ".wasm"
    exe_extension = ".wasm"
    static_lib_extension = ".wasm"

    _cxx_extensions = [".cpp", ".cc", ".cxx", ".c++"]

    def __init__(self, verbose=0, dry_run=0, force=0):
        super().__init__(verbose, dry_run, force)

        self.cc = str(WASI_SDK / "bin" / "wasm32-wasip1-threads-clang")
        self.cxx = str(WASI_SDK / "bin" / "wasm32-wasip1-threads-clang++")
        self.ld = str(WASI_SDK / "bin" / "wasm-ld")

        self.cc = self.cc.replace("\\", "/")
        self.cxx = self.cxx.replace("\\", "/")
        self.ld = self.ld.replace("\\", "/")

        self.set_executables(
            compiler=f"{self.cc} -Wall",
            compiler_so=f"{self.cc} -Wall",
            compiler_cxx=f"{self.cxx} -Wall",
            linker_exe=f"{self.ld} --no-entry --export-dynamic --allow-undefined",
            linker_so=f"{self.ld} --no-entry --export-dynamic --allow-undefined",
        )

    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        compiler = (
            self.compiler_cxx if ext in self._cxx_extensions else self.compiler_so
        )
        try:
            self.spawn(compiler + cc_args + [src, "-o", obj] + extra_postargs)

        except ExecError as msg:
            raise CompileError(msg)

    def link(
        self,
        target_desc,
        objects,
        output_filename,
        output_dir=None,
        libraries=None,
        library_dirs=None,
        runtime_library_dirs=None,
        export_symbols=None,
        debug=0,
        extra_preargs=None,
        extra_postargs=None,
        build_temp=None,
        target_lang=None,
    ):
        # force target language to c
        return super().link(
            target_desc,
            objects,
            output_filename,
            output_dir,
            libraries,
            library_dirs,
            runtime_library_dirs,
            export_symbols,
            debug,
            extra_preargs,
            extra_postargs,
            build_temp,
            "c",
        )
