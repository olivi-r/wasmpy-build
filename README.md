# WasmPy-Build

This tool can compile CPython C extension files, such as the ones created by Cython, to WebAssembly so that the extensions are platform independent.

The created `.wasm` files can be imported by [WasmPy](https://github.com/olivi-r/wasmpy) in a simmilar manner to native C extensions.

This project contains modified CPython header files as well as a build script to ease the creation of `.wasm` extension files.

Currently this project only supports CPython 3.8, 3.9 and 3.10 but I'm hoping to add support for older versions.

# Installation

To install WasmPy-Build you will first need to install the [Emscripten SDK](https://emscripten.org/docs/getting_started/downloads.html#installation-instructions).

### Install WasmPy-Build from pip

```bash
$ pip install wasmpy-build
```

### ... or build from source

```bash
$ git clone --recurse-submodules https://github.com/olivi-r/wasmpy-build
$ cd wasmpy-build
$ python -m pip install -r requirements.txt
$ python patch_headers.py
$ python setup.py install
```
