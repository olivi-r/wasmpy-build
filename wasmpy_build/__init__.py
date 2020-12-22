import os, platform, subprocess, sys


def build():
    command = sys.argv[1:]

    # find cpython include files
    include_dir = os.path.join(os.path.dirname(__file__), "include", "cp")
    version = "".join(str(i) for i in sys.version_info[:2])
    include_dir += version

    emcc = "emcc.bat" if platform.system() == "Windows" else "emcc"
    args = [
        emcc, "-Wno-visibility", f"-I{include_dir}",
        "-sSIDE_MODULE", "-sSTANDALONE_WASM", "-DSIZEOF_WCHAR_T",
    ]
    try:
        subprocess.call(args + command)

    except FileNotFoundError:
        print("emsdk not found\nYou can install it from https://github.com/ems\
cripten-core/emsdk\nIf it is already installed make sure to call the emsdk_env\
.sh/emsdk_env.bat script or add emsdk to path.")


if __name__ == "__main__":
    build()
