from setuptools._distutils.unixccompiler import UnixCCompiler

from .core import WASI_SDK


class ClangWASICompiler(UnixCCompiler):
    compiler_type = "clang-wasi"
    shared_lib_extension = ".wasm"
    exe_extension = ".wasm"
    static_lib_extension = ".wasm"

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
