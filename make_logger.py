import logging
import logging.config
import pathlib
from pathlib import Path
import functools
import sys, os
from datetime import datetime


def make_logger(filename: str, path: pathlib.Path=Path.cwd().resolve()):
    """
    src: https://realpython.com/python-logging/

    Args:
        filename (str, optional): Path to file calling make_logger.
        path (pathlib.Path, optional): Path where the log file is saved. Defaults to None.

    Returns:
        [type]: [description]
    """

    
    logging.config.fileConfig(f'logging.conf', disable_existing_loggers=False)
    logger = logging.getLogger()

    filename = f"{Path(filename).stem}_{datetime.now().date()}_{datetime.now().time()}.log"
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
