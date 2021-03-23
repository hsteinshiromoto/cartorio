from src.make_logger import log_fun, make_logger
import logging
from datetime import datetime
from pathlib import Path

LOGGER, FILENAME = make_logger(__file__, test=True)

@log_fun
def divide(num1, num2):
    return num1 / num2


@log_fun
def multiply(num1, num2):
    return num1 * num2


def test_logfile():
    assert Path(FILENAME).is_file() == True


if __name__ == '__main__':

    result = divide(10, 0)

    LOGGER.info("Again")
    
    result = multiply(10, 1)