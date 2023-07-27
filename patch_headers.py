import os, shutil, subprocess
import patch

# current tags for versions
vers = {
    "3.8": "v3.8.17",
    "3.9": "v3.9.17",
    "3.10": "v3.10.12",
    "3.11": "v3.11.4",
}


for patch_file in os.listdir("patches"):
    ver = os.path.splitext(patch_file)[0]
    ver_tag = "cp" + "".join(ver.split("."))

    subprocess.check_call(["git", "-C", "cpython", "checkout", vers[ver]])

    # copy headers and license
    shutil.copytree("cpython/Include", f"wasmpy_build/include/{ver_tag}")
    shutil.copy2("pyconfig.h", f"wasmpy_build/include/{ver_tag}/pyconfig.h")
    shutil.copy2("cpython/LICENSE", f"wasmpy_build/include/{ver_tag}/LICENSE")

    # patch headers
    patches = patch.fromfile(os.path.join("patches", patch_file))
    patches.apply(root=f"wasmpy_build/include/{ver_tag}")
