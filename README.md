# 1. Cartorio

A wrapper on the `logging` module for Python that provides a simple and easy to use interface for logging.

# 2. Contents
- [1. Cartorio](#1-cartorio)
- [2. Contents](#2-contents)
- [3. Installation](#3-installation)
- [4. Usage](#4-usage)

# 3. Installation
```bash
pip install cartorio
```

# 4. Usage
1. Import module as `from cartorio import log, fun`
2. Instantiate logger in the `__name__ == "__main__"` section of each script as `logger = log(*args)`.
3. Use the decorator `@fun` to log in and out of each function.