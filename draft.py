import logging
import logging.config
import pathlib
from pathlib import Path
import functools
import sys, os


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
