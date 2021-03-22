import functools
import inspect
import logging
import logging.config
import os
import pathlib
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8'))


def make_logger(filename: str, path: pathlib.Path=PROJECT_ROOT / "logs", test: bool=False):
    """
    Instantiate logger object

    Args:
        filename (str): Path to file calling make_logger.
        path (pathlib.Path, optional): Path where the log file is saved. Defaults to logs/.
        test (bool): Return filename

    Returns:
        [type]: [description]

    References:
        [1] https://realpython.com/python-logging/
    """
    logging.config.fileConfig(str(PROJECT_ROOT / "conf" / "logging.conf"), disable_existing_loggers=False)
    logger = logging.getLogger()

    filename = f"{Path(filename).stem}_{datetime.now().date()}_{datetime.now().time()}.log"
    fh = logging.FileHandler(str(path / f'{filename}'))
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)-16s || %(name)s || %(process)d || %(levelname)s || %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    if test == True:
        return logger, str(path / f'{filename}')

    else:
        return logger


def log_fun(func):
    """
    Log a functions input and outputs

    Args:
        func (callable): Callable to to be logged

    Returns:
        Callable: Callable outputs

    References:
        [1] https://dev.to/aldo/implementing-logging-in-python-via-decorators-1gje
    """
    logger = logging.getLogger()

    func_filename = inspect.currentframe().f_back.f_code.co_filename #Filename where the function is called from
    func_lineno = inspect.currentframe().f_back.f_lineno             #TODO: Line of filename where the function is called from

    entering_time = datetime.now()
    logger.info(f"{Path(func_filename).name} || {func.__module__} || {func_lineno} || Entering {func.__name__}")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:                
            return func(*args, **kwargs)

        except Exception:
            error_msg = f"In {func.__name__}"
            logger.exception(error_msg, exc_info=True)

        finally:
            leaving_time = datetime.now()
            logger.info(f"{func.__module__} || {func_lineno} || Leaving {func.__name__} || Elapsed: {leaving_time - entering_time}")

    return wrapper
