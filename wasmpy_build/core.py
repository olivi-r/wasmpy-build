import pathlib
import platform
import shutil
import subprocess
import sys
import tarfile

import appdirs
import requests
import tqdm


# configure include and compiler paths

CPYTHON_INCLUDE_DIR = pathlib.Path(__file__).parent / "include" / "cp" + "".join(
    str(i) for i in sys.version_info[:2]
)

WASI_SDK = pathlib.Path(appdirs.user_data_dir("wasmpy-build", "wasmpy")) / "wasi-sdk"

CC = WASI_SDK / "bin" / "wasm32-wasip1-threads-clang"
CXX = WASI_SDK / "bin" / "wasm32-wasip1-threads-clang++"


# default compiler options

DEFAULT_OPTS = [
    "-pthread",
    "-O2",
    "-Wall",
    "-nostartfiles",
    "-Wl,--no-entry,-export-dynamic,--allow-undefined",
    f"-I{CPYTHON_INCLUDE_DIR}",
]


def build(options, is_cpp=False):
    cmd = [CXX if is_cpp else CC] + DEFAULT_OPTS + options

    print(" ".join(cmd))
    try:
        subprocess.call(cmd)

    except FileNotFoundError:
        print("wasi-sdk not found")
        download_sdk(build, options, is_cpp)


def download_sdk(before=None, *before_args):
    WASI_SDK.mkdir(parents=True, exist_ok=True)

    url = "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-22/"
    if platform.system() == "Windows":
        file = "wasi-sdk-22.0.m-mingw64.tar.gz"

    elif platform.system() == "Linux":
        file = "wasi-sdk-22.0-linux.tar.gz"

    url += file
    if not (WASI_SDK.parent / file).exists():
        print(f"Downloading {file}")
        with requests.get(url, stream=True) as req:
            req.raise_for_status()

            with (WASI_SDK.parent / file).open("wb+") as fp, tqdm.tqdm(
                desc=file,
                total=int(req.headers.get("content-length", 0)),
                unit="MiB",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress:
                for chunk in req.iter_content(4096):
                    progress.update(fp.write(chunk))

    print(f"Extracting {file}")
    with tarfile.open(WASI_SDK.parent / file) as tar:
        extracted = tar.getnames()[0]
        tar.extractall(WASI_SDK)

    shutil.move(WASI_SDK.parent / extracted, WASI_SDK)

    # version file to avoid using outdated wasi-sdk
    with open(WASI_SDK.parent / "wasi-sdk-version.txt", "w+") as fp:
        fp.write("22")

    print(f"wasi-sdk installed at: {WASI_SDK}")
    if before is not None:
        before(*before_args)
