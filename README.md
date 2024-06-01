# wasmpy-build

[![appveyor-build](https://img.shields.io/appveyor/build/olivi-r/wasmpy-build?logo=appveyor)](https://ci.appveyor.com/project/olivi-r/wasmpy-build)

This tool can compile CPython C extension files, such as the ones created by Cython, to WebAssembly so that the extensions are platform independent.

Currently supports CPython 3.6 to 3.12.

[wasi-sdk](https://github.com/WebAssembly/wasi-sdk) is automatically downloaded on first use.

# Usage

Wasmpy-build can be easily integrated into an existing project by the use of a drop-in `build_ext` override:

## From a `setup.py` script

```python
from wasmpy_build import build_ext
from setuptools import setup, Extension


setup(
    ext_modules=[Extension("mymodule", ["mymodule.c"])],
    cmdclass={"build_ext": build_ext},
)
```

This also works with generated sources, like from Cython:

```python
from Cython.Build import cythonize
from wasmpy_build import build_ext
from setuptools import setup, Extension

setup(
    ext_modules=cythonize([
        Extension("mymodule", ["mymodule.pyx"])
    ]),
    cmdclass={"build_ext": build_ext},
)
```

## From the command line

### C

```bash
wasmpy-build my_file.c -o my_file.wasm
```

### C++

```bash
wasmpy-build++ my_file.cpp -o my_file.wasm
```

or

```bash
wasmpy-build-cpp my_file.cpp -o my_file.wasm
```

# Installation

### Install with pip

```bash
pip install wasmpy-build
```

### Build from source

```bash
git clone --recurse-submodules https://github.com/olivi-r/wasmpy-build
cd wasmpy-build
python generate.py
python -m pip install .
```
