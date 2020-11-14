import logging
import logging.config
import pathlib
from pathlib import Path
import functools
import sys, os

def _make_logger(filename: str=f"{__name__}.log", path: pathlib.Path=None):
    """
    src: https://realpython.com/python-logging/

    Args:
        filename (str, optional): [description]. Defaults to f"{__name__}.log".
        path (pathlib.Path, optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """

    # Create a custom logger
    logger = logging.getLogger()

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler(filename)
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.ERROR)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    f_format = logging.Formatter('%(asctime)s | %(name)s | %(process)d | %(levelname)s | %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


def make_logger(filename: str=f"{__name__}.log", path: pathlib.Path=None):
    """
    src: https://realpython.com/python-logging/

    Args:
        filename (str, optional): [description]. Defaults to f"{__name__}.log".
        path (pathlib.Path, optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """

    # Create a custom logger
    logging.config.fileConfig(f'logging.conf', disable_existing_loggers=False)
    logger = logging.getLogger()

    return logger


def log_fun(func):
    """
    src https://dev.to/aldo/implementing-logging-in-python-via-decorators-1gje

    We create a parent function to take arguments
    :param path:
    :return:
    """
    logger = logging.getLogger()
    logger.info(f"Entering {func.__name__}")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:                
            return func(*args, **kwargs)

        except Exception:
            error_msg = f"In {func.__name__}"
            logger.exception(error_msg, exc_info=True)

        finally:
            logger.debug(f"Leaving {func.__name__}")
            return

    return wrapper
