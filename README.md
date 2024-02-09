# wasmpy-build

This tool can compile CPython C extension files, such as the ones created by Cython, to WebAssembly so that the extensions are platform independent.

Currently this project only supports CPython 3.8, 3.9, 3.10, 3.11 and 3.12 but I'm hoping to add support for older and future versions.

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
python generate.py
python -m pip install .
```

# Usage

Pass the file with any extra arguments to the console scripts:

### C

```bash
wasmpy-build my_file.c -o my_file.wasm
```

### C++

```bash
wasmpy-build-cpp my_file.cpp -o my_file.wasm
```
