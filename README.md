#  HipopyBind : HIPO PyBind11 Library
[![PyPI](https://img.shields.io/pypi/v/hipopybind.svg)](https://pypi.org/project/hipopybind/)
[![Python](https://github.com/mfmceneaney/hipopybind/actions/workflows/python.yml/badge.svg)](https://github.com/mfmceneaney/hipopybind/actions/workflows/python.yml)

This project exposes in python the [hipo](https://github.com/gavalian/hipo) classes and a few
custom classes and functions from C++ via [pybind11](https://github.com/pybind/pybind11).

## Prerequisites

* Python >=3.9
* A compiler with C++17 support
* Ninja or Pip 10+
* meson

## :green_circle: Installation

To install from PyPi run:

```bash
pip install hipopybind
```

Compiling the library from source is **platform dependent**.

On macos run:
```bash
git clone --recurse-submodules https://github.com/mfmceneaney/hipopybind.git
cd hipopybind
pip install poetry delocate
poetry build
delocate -w repaired_dist/ dist/*.whl
pip install repaired_dist/*.whl
```

On linux run:

```bash
git clone --recurse-submodules https://github.com/mfmceneaney/hipopybind.git
cd hipopybind
pip install poetry auditwheel
poetry build
auditwheel repair -w repaired_dist/ dist/*.whl
pip install repaired_dist/*.whl
```

# :rocket: Getting Started

Run the tutorials via:
```bash
python3 tutorials/write.py
python3 tutorials/read.py
```

#

Contact: matthew.mceneaney@duke.edu
