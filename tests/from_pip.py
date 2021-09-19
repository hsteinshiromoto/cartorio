import sys
from pathlib import Path

from cartorio.log import fun, log

logger = log(filename=Path(__file__).resolve().stem, logs_path=Path(__file__).resolve().parent)


@fun
def divide(num1, num2):
    return num1 / num2

@fun
def multiply(num1, num2):
    return num1 * num2

multiply(10, 1)
try:
    divide(10, 0)

except ZeroDivisionError as e:
    print(sys.exc_info())