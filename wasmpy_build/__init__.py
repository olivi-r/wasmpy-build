import os, platform, shutil, subprocess, sys, tarfile
import appdirs, requests, tqdm


sdk_dir = os.path.join(appdirs.user_data_dir("wasmpy-build", "wasmpy"))


def download_sdk(before=None):
    try:
        os.makedirs(sdk_dir)

    except FileExistsError:
        pass

    url = (
        "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-20/"
    )
    if platform.system() == "Windows":
        file = "wasi-sdk-20.0.m-mingw.tar.gz"

    elif platform.system() == "Linux":
        file = "wasi-sdk-20.0-linux.tar.gz"

    url += file
    if not os.path.exists(os.path.join(sdk_dir, file)):
        print(f"Downloading {file}")
        with requests.get(url, stream=True) as req:
            req.raise_for_status()

            with open(os.path.join(sdk_dir, file), "wb+") as fp, tqdm.tqdm(
                desc=file,
                total=int(req.headers.get("content-length", 0)),
                unit="MiB",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress:
                for chunk in req.iter_content(4096):
                    progress.update(fp.write(chunk))

    print(f"Extracting {file}")
    with tarfile.open(os.path.join(sdk_dir, file)) as tar:
        extracted = tar.getnames()[0]
        tar.extractall(sdk_dir)

    shutil.move(
        os.path.join(sdk_dir, extracted),
        os.path.join(sdk_dir, f"sdk-{platform.system()}"),
    )

    print(f"wasi-sdk installed at: {os.path.join(sdk_dir, 'sdk')}")
    if before is not None:
        before()


def buildc():
    command = sys.argv[1:]

    # find cpython include files
    include_dir = os.path.join(os.path.dirname(__file__), "include", "cp")
    version = "".join(str(i) for i in sys.version_info[:2])
    include_dir += version

    args = [
        f"{sdk_dir}/sdk-{platform.system()}/bin/clang",
        f"--sysroot={sdk_dir}/sdk-{platform.system()}/share/wasi-sysroot",
        "--target=wasm32-wasi-threads",
        "-pthread",
        "-nostartfiles",
        f"-I{include_dir}",
        "-Wl,--no-entry,-export-dynamic,--allow-undefined",
    ] + command

    print(" ".join(args))
    try:
        subprocess.call(args)

    except FileNotFoundError:
        print("wasi-sdk not found")
        download_sdk(buildc)


def buildcpp():
    command = sys.argv[1:]

    # find cpython include files
    include_dir = os.path.join(os.path.dirname(__file__), "include", "cp")
    version = "".join(str(i) for i in sys.version_info[:2])
    include_dir += version

    args = [
        f"{sdk_dir}/sdk-{platform.system()}/bin/clang++",
        f"--sysroot={sdk_dir}/sdk-{platform.system()}/share/wasi-sysroot",
        "--target=wasm32-wasi-threads",
        "-pthread",
        "-nostartfiles",
        f"-I{include_dir}",
        "-Wl,--no-entry,-export-dynamic,--allow-undefined",
    ] + command

    print(" ".join(args))
    try:
        subprocess.call(args)

    except FileNotFoundError:
        print("wasi-sdk not found")
        download_sdk(buildcpp)
