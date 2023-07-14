# wasmpy-build

This tool can compile CPython C extension files, such as the ones created by Cython, to WebAssembly so that the extensions are platform independent.

This project contains modified CPython header files as well as a build script to ease the creation of `.wasm` extension files.

Currently this project only supports CPython 3.8, 3.9, 3.10 and 3.11 but I'm hoping to add support for older and future versions.

The project will automatically download [wasi-sdk](https://github.com/WebAssembly/wasi-sdk) on first use.

# Installation
### Install from pip

```bash
pip install wasmpy-build
```

### or build from source

```bash
git clone --recurse-submodules https://github.com/olivi-r/wasmpy-build
cd wasmpy-build
pip install patch
python patch_headers.py
python -m pip install .
```

# Usage

Simply pass the C or C++ file and any extra arguments straight to the compiler.

```bash
wasmpy-build my_file.c -o my_file.wasm
```
