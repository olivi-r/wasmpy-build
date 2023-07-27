import os, setuptools


with open("README.md") as fp:
    long_description = fp.read()


def recurse_files(directory):
    paths = []
    for path, _, files in os.walk(directory):
        for file in files:
            paths.append(os.path.join("..", path, file))

    return paths


setuptools.setup(
    name="wasmpy-build",
    version="0.4.0",
    author="Olivia Ryan",
    author_email="olivia.r.dev@gmail.com",
    description="WebAssembly build tool for CPython C extensions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olivi-r/wasmpy-build",
    packages=["wasmpy_build"],
    package_data={"wasmpy_build": recurse_files("wasmpy_build/include")},
    entry_points={
        "console_scripts": [
            "wasmpy-build=wasmpy_build:buildc",
            "wasmpy-build++=wasmpy_build:buidcpp",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    python_requires=">=3.8",
    install_requires=["appdirs", "requests", "tqdm"],
)
