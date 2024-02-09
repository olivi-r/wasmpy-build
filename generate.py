import shutil
import subprocess


# current tags for versions
versions = {
    "3.6": "v3.6.15",
    "3.7": "v3.7.17",
    "3.8": "v3.8.18",
    "3.9": "v3.9.18",
    "3.10": "v3.10.13",
    "3.11": "v3.11.8",
    "3.12": "v3.12.2",
}


shutil.rmtree("wasmpy_build/include", ignore_errors=True)

for version in versions:
    version_tag = "cp" + "".join(version.split("."))

    subprocess.check_call(["git", "-C", "cpython", "checkout", versions[version]])

    # copy headers and license
    shutil.copytree("cpython/Include", f"wasmpy_build/include/{version_tag}")
    shutil.copy2("pyconfig.h", f"wasmpy_build/include/{version_tag}/pyconfig.h")
    shutil.copy2("cpython/LICENSE", f"wasmpy_build/include/{version_tag}/LICENSE")
