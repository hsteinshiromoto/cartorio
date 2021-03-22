from src.make_logger import log_fun, make_logger
import logging
from datetime import datetime
from pathlib import Path

LOGGER, FILENAME = make_logger(__file__, test=True)

#! Todo: Improve this module to do all test

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

    """
    Fix bug

    Expected:
        2021-Mar-22 17:38:03.480 || root || INFO || test_logger.py || __main__ || 26 || Entering divide
        2021-Mar-22 17:38:03.481 || root || ERROR || In divide
        Traceback (most recent call last):
        File "/Users/humberto/Projects/logger/src/make_logger.py", line 73, in wrapper
            return func(*args, **kwargs)
        File "/Users/humberto/Projects/logger/test_logger.py", line 12, in divide
            return num1 / num2
        ZeroDivisionError: division by zero
        2021-Mar-22 17:38:03.481 || root || INFO || __main__ || 26 || Leaving divide || Elapsed: 0:00:00.001196
        2021-Mar-22 17:38:03.482 || root || INFO || Again
        2021-Mar-22 17:38:03.481 || root || INFO || test_logger.py || __main__ || 30 || Entering multiply
        2021-Mar-22 17:38:03.482 || root || INFO || __main__ || 30 || Leaving multiply || Elapsed: 0:00:00.001131

    Got:
        2021-Mar-22 17:38:03.480 || root || INFO || test_logger.py || __main__ || 11 || Entering divide
        2021-Mar-22 17:38:03.481 || root || INFO || test_logger.py || __main__ || 16 || Entering multiply
        2021-Mar-22 17:38:03.481 || root || ERROR || In divide
        Traceback (most recent call last):
        File "/Users/humberto/Projects/logger/src/make_logger.py", line 73, in wrapper
            return func(*args, **kwargs)
        File "/Users/humberto/Projects/logger/test_logger.py", line 12, in divide
            return num1 / num2
        ZeroDivisionError: division by zero
        2021-Mar-22 17:38:03.481 || root || INFO || __main__ || 11 || Leaving divide || Elapsed: 0:00:00.001196
        2021-Mar-22 17:38:03.482 || root || INFO || Again
        2021-Mar-22 17:38:03.482 || root || INFO || __main__ || 16 || Leaving multiply || Elapsed: 0:00:00.001131
    """