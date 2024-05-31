import os
import platform
import shutil
import subprocess
import sys
import tarfile

import appdirs
import requests
import tqdm


# find cpython include files

CPYTHON_INCLUDE_DIR = os.path.join(
    os.path.dirname(__file__), "include", "cp"
) + "".join(str(i) for i in sys.version_info[:2])

WASI_SDK_DIR = os.path.join(appdirs.user_data_dir("wasmpy-build", "wasmpy"))


def buildc(options):
    args = [
        f"{WASI_SDK_DIR}/sdk-{platform.system()}/bin/clang",
        f"--sysroot={WASI_SDK_DIR}/sdk-{platform.system()}/share/wasi-sysroot",
        "--target=wasm32-wasi-threads",
        "-pthread",
        "-nostartfiles",
        f"-I{CPYTHON_INCLUDE_DIR}",
        "-Wl,--no-entry,-export-dynamic,--allow-undefined",
    ] + options

    print(" ".join(args))
    try:
        subprocess.call(args)

    except FileNotFoundError:
        print("wasi-sdk not found")
        download_sdk(buildc, options)


def buildcpp(options):
    args = [
        f"{WASI_SDK_DIR}/sdk-{platform.system()}/bin/clang++",
        f"--sysroot={WASI_SDK_DIR}/sdk-{platform.system()}/share/wasi-sysroot",
        "--target=wasm32-wasi-threads",
        "-pthread",
        "-nostartfiles",
        f"-I{CPYTHON_INCLUDE_DIR}",
        "-Wl,--no-entry,-export-dynamic,--allow-undefined",
    ] + options

    print(" ".join(args))
    try:
        subprocess.call(args)

    except FileNotFoundError:
        print("wasi-sdk not found")
        download_sdk(buildcpp, options)


def download_sdk(before=None, before_opts=[]):
    try:
        os.makedirs(WASI_SDK_DIR)

    except FileExistsError:
        pass

    url = "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-22/"
    if platform.system() == "Windows":
        file = "wasi-sdk-22.0.m-mingw64.tar.gz"

    elif platform.system() == "Linux":
        file = "wasi-sdk-22.0-linux.tar.gz"

    url += file
    if not os.path.exists(os.path.join(WASI_SDK_DIR, file)):
        print(f"Downloading {file}")
        with requests.get(url, stream=True) as req:
            req.raise_for_status()

            with open(os.path.join(WASI_SDK_DIR, file), "wb+") as fp, tqdm.tqdm(
                desc=file,
                total=int(req.headers.get("content-length", 0)),
                unit="MiB",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress:
                for chunk in req.iter_content(4096):
                    progress.update(fp.write(chunk))

    print(f"Extracting {file}")
    with tarfile.open(os.path.join(WASI_SDK_DIR, file)) as tar:
        extracted = tar.getnames()[0]
        tar.extractall(WASI_SDK_DIR)

    shutil.move(
        os.path.join(WASI_SDK_DIR, extracted),
        os.path.join(WASI_SDK_DIR, f"sdk-{platform.system()}"),
    )

    print(f"wasi-sdk installed at: {os.path.join(WASI_SDK_DIR, 'sdk')}")
    if before is not None:
        before(before_opts)
