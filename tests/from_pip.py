import sys
from pathlib import Path

from cartorio import log, make_logger

# Tests installation from pip

# Test instantiation of log file
logger, _ = make_logger(filename=Path(__file__).resolve().stem, logs_path=Path(__file__).resolve().parent)

@log
def divide(num1, num2):
    return num1 / num2

@log
def multiply(num1, num2):
    return num1 * num2

# Test if entry and exit log messages are correct
multiply(10, 1)
try:
    divide(10, 0)

except ZeroDivisionError as e:
    # Test if raised error is correct
    print(sys.exc_info())
