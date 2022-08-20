import subprocess
import shutil
import patch
import os


for patch_file in os.listdir("patches"):
    ver = os.path.splitext(patch_file)[0]
    ver_tag = "cp" + "".join(ver.split("."))

    subprocess.check_call(f"git -C cpython checkout {ver}")

    # copy headers and license
    shutil.copytree("cpython/Include", f"wasmpy_build/include/{ver_tag}")
    shutil.copy2("cpython/LICENSE", f"wasmpy_build/include/{ver_tag}/LICENSE")

    # patch headers
    patches = patch.fromfile(os.path.join("patches", patch_file))
    patches.apply(root=f"wasmpy_build/include/{ver_tag}")
