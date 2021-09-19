from logging import Logger
from pathlib import Path

from cartorio.log import fun, log

logger = log(file=Path(__file__).resolve().stem, logs_path=Path(__file__).resolve().parent)


@fun
def divide(num1, num2):
    return num1 / num2

@fun
def multiply(num1, num2):
    return num1 * num2

divide(10, 0)
multiply(10, 1)
