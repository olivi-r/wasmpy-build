import json
import pathlib
import platform
import shutil
import subprocess
import sys
import tarfile

import appdirs
import requests
import tqdm


WASI_SDK = pathlib.Path(appdirs.user_data_dir("wasmpy-build", "wasmpy")) / "wasi-sdk"

# configure include and compiler paths
CPYTHON_INCLUDE_DIR = (
    pathlib.Path(__file__).parent
    / "include"
    / ("cp" + "".join(str(i) for i in sys.version_info[:2]))
)

CC = WASI_SDK / "bin" / "wasm32-wasip1-threads-clang"
CXX = WASI_SDK / "bin" / "wasm32-wasip1-threads-clang++"
if platform.system() == "Windows":
    CC = CC.parent / (CC.name + ".exe")
    CXX = CXX.parent / (CXX.name + ".exe")

# default compiler options
DEFAULT_OPTS = [
    "-pthread",
    "-O2",
    "-Wall",
    "-nostartfiles",
    "-Wl,--no-entry,-export-dynamic,--allow-undefined",
    f"-I{CPYTHON_INCLUDE_DIR}",
]

# library path
WASI_LIB_DIR = WASI_SDK / "share" / "wasi-sysroot" / "lib" / "wasm32-wasip1-threads"


def build(options, is_cpp=False):
    cmd = [CXX if is_cpp else CC]
    if not cmd[0].exists():
        download_sdk()

    cmd += DEFAULT_OPTS + options

    print(" ".join(map(str, cmd)))
    subprocess.call(cmd)


def download_sdk():
    WASI_SDK.parent.mkdir(parents=True, exist_ok=True)

    # get download URL
    url = "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-22/"
    if platform.system() == "Windows":
        file = "wasi-sdk-22.0.m-mingw64.tar.gz"

    elif platform.system() == "Linux":
        file = "wasi-sdk-22.0-linux.tar.gz"

    url += file

    # download the SDK
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

    # extract the SDK tarball
    print(f"Extracting {file}")
    with tarfile.open(WASI_SDK.parent / file) as tar:
        extracted = tar.getnames()[0]
        tar.extractall(WASI_SDK.parent)

    shutil.move(WASI_SDK.parent / extracted, WASI_SDK)

    # delete the tarball
    (WASI_SDK.parent / file).unlink()

    # version file to avoid using outdated SDKs
    if (WASI_SDK.parent / "versions.json").exists():
        with (WASI_SDK.parent / "versions.json").open("r") as fp:
            versions = json.load(fp)

    else:
        versions = {}

    versions.update({"wasi-sdk": 22})
    with (WASI_SDK.parent / "versions.json").open("w+") as fp:
        json.dump(versions, fp)

    print(f"wasi-sdk installed at: {WASI_SDK}")
