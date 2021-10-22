[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5563175.svg)](https://doi.org/10.5281/zenodo.5563175)
[![Documentation Status](https://readthedocs.org/projects/cartorio/badge/?version=latest)](https://cartorio.readthedocs.io/?badge=latest)


# 1. Cartorio

A wrapper on the `logging` module for Python that provides a simple and easy to use interface for logging.

# 2. Contents
- [1. Cartorio](#1-cartorio)
- [2. Contents](#2-contents)
- [3. Installation](#3-installation)
- [4. Documentation](#4-documentation)
- [5. Usage](#5-usage)

# 3. Installation
```bash
pip install cartorio
```

# 4. Documentation

https://cartorio.readthedocs.io/en/latest/

# 5. Usage
Example:

```python
import sys
from pathlib import Path

from cartorio import fun, log

# Test instantiation of log file
logger = log(filename=Path(__file__).resolve().stem, logs_path=Path(__file__).resolve().parent)

@fun
def multiply(num1, num2):
    return num1 * num2

# Test if entry and exit log messages are correct
multiply(10, 1)
```