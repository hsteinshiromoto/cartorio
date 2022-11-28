[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5563175.svg)](https://doi.org/10.5281/zenodo.5563175)
[![Documentation Status](https://readthedocs.org/projects/cartorio/badge/?version=stable)](https://cartorio.readthedocs.io/en/stable/?badge=stable)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hsteinshiromoto/cartorio?style=flat)
![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)

# 1. Cartorio

A wrapper on the `logging` module for Python that provides a simple and easy-to-use interface for logging.

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

https://cartorio.readthedocs.io/en/stable/

# 5. Usage

Consider that your project consists of two scripts:

```bash
parent.py
child/
└──  child.py
```

An example of these scripts are:
```python
# parent.py

from pathlib import Path
from cartorio import make_logger, log

from child.child import multiply

@log
def main()
    multiply(10, 1)

if __name__ == "__main__":
    # Instantiation of log file
    logger, _ = make_logger(filename=Path(__file__).resolve().stem, logs_path=Path(__file__).resolve().parent)
    # where,
    # filename (str, Path): Log file.
    # logs_path (Path): Path where the log file is saved to.
    main()
```

```python
# child.py

from cartorio import fun, log

@log
def multiply(num1, num2):
    return num1 * num2
```

The log filename will be `parent_<timestamp>.log` and it will contain the information in the form
```
<timestamp> || root || 30664 || INFO || parent.py || parent || <line_number> || Enter || multiply
<timestamp> || root || 30664 || INFO || parent.py || parent || <line_number> || Leave || multiply || Elapsed: 0:00:00.001708
```