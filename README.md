[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5563175.svg)](https://doi.org/10.5281/zenodo.5563175)
[![Documentation Status](https://readthedocs.org/projects/cartorio/badge/?version=stable)](https://cartorio.readthedocs.io/en/stable/?badge=stable)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hsteinshiromoto/cartorio?style=flat)
![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)
[![PyPI version](https://badge.fury.io/py/cartorio.svg)](https://badge.fury.io/py/cartorio)

# 1. Cartorio

A structured logging library for Python built on [structlog](https://www.structlog.org/). It provides a simple decorator and logger factory that emit structured events in either human-friendly console format (development) or JSON (production).

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

from cartorio import make_logger, log

from child.child import multiply

@log
def main():
    multiply(10, 1)

if __name__ == "__main__":
    # Get a structlog bound logger (logs_path is no longer needed)
    logger, _ = make_logger(__file__)
    logger.info("starting", app="parent")
    main()
```

```python
# child.py

from cartorio import log, get_logger

logger = get_logger(__name__)

@log
def multiply(num1, num2):
    logger.info("multiplying", num1=num1, num2=num2)
    return num1 * num2
```

By default, output is rendered as coloured console text suitable for development:
```
2024-01-01T12:00:00.000000Z [info     ] enter   [parent] function=main filename=parent.py module=__main__
2024-01-01T12:00:00.001000Z [info     ] leave   [parent] elapsed=0:00:00.001000 function=main module=__main__
```

To emit one JSON object per line (e.g. for log aggregation in production), set the `LOG_FORMAT` environment variable:

```bash
LOG_FORMAT=json python parent.py
```

```json
{"level": "info", "logger": "__main__", "timestamp": "2024-01-01T12:00:00.000000Z", "event": "enter", "function": "main", "filename": "parent.py", "module": "__main__"}
{"level": "info", "logger": "__main__", "timestamp": "2024-01-01T12:00:00.001000Z", "event": "leave", "function": "main", "elapsed": "0:00:00.001000", "module": "__main__"}
```

The `@log` decorator also accepts two optional keyword arguments:

### `@log(level="debug")`

Log ``"enter"`` and ``"leave"`` events at ``debug`` level instead of the default ``info``. ``"error"`` events always use ``exception``.

```python
@log(level="debug")
def compute(x: int) -> int:
    return x ** 2
```

### `@log(log_args=True)`

Include function argument values in the ``"enter"`` event. Values are rendered with ``repr()``.

```python
@log(log_args=True)
def create_user(name: str, age: int, admin: bool = False):
    return {"name": name, "age": age, "admin": admin}
```

Console output:
```
2024-01-01T12:00:00.000000Z [info     ] enter   function=create_user module=__main__ filename=app.py args={'name': 'Alice', 'age': 30, 'admin': True}
2024-01-01T12:00:00.001000Z [info     ] leave   function=create_user module=__main__ elapsed=0:00:00.001000
```

Both options can be combined:

```python
@log(level="debug", log_args=True)
def expensive_query(user_id: int) -> list:
    ...
```
