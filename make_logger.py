import logging
import logging.config
import pathlib
from pathlib import Path
import functools
import sys, os
from datetime import datetime


def make_logger(logger_name: str, filename: str=f"{datetime.now().date()}_{datetime.now().time()}.log"
                ,path: pathlib.Path=Path.cwd().resolve()):
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

    fh = logging.FileHandler(str(path / f'{filename}'))
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)-16s || %(name)s || %(process)d || %(levelname)s || %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger


def log_fun(func):
    """
    src https://dev.to/aldo/implementing-logging-in-python-via-decorators-1gje

    We create a parent function to take arguments
    :param path:
    :return:
    """
    logger = logging.getLogger()
    entering_time = datetime.now()
    logger.info(f"Entering {func.__name__}")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:                
            return func(*args, **kwargs)

        except Exception:
            error_msg = f"In {func.__name__}"
            logger.exception(error_msg, exc_info=True)

        finally:
            leaving_time = datetime.now()
            logger.info(f"Leaving {func.__name__} | Elapsed: {leaving_time - entering_time}")

    return wrapper
