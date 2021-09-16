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
from typing import Callable

PROJECT_ROOT = Path(subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                    stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8'))


def make_logs_path(path: Path = PROJECT_ROOT / "logs") -> Path:
    """
    Create logs directory if it doesn't exist

    Args:
        path (Path, optional): Path where the log file is saved. Defaults to PROJECT_ROOT/logs/.
        test (bool): Return filename

    Returns:
        (Path): Path to logs directory

    Example:
        >>> make_logs_path()
        PROJECT_ROOT / "logs"
    """
    path.mkdir(parents=True, exist_ok=True)

    return


def make_logger(log_config_file: Path = PROJECT_ROOT / "cartorio" / "conf" / "logging.conf"):

    logging.config.fileConfig(str(log_config_file),
                              disable_existing_loggers=False)

    return logging.getLogger()


def make_handler(filename: str, logs_path: Path, log_format: str):

    fh = logging.FileHandler(str(logs_path / f'{filename}'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_format)

    return fh


def log_fun(func: Callable):
    """
    Log a callable

    Args:
        func (callable): Callable to be logged

    Returns:
        Callable: Callable outputs

    References:
        [1] https://dev.to/aldo/implementing-logging-in-python-via-decorators-1gje
        [2] https://stackoverflow.com/questions/6810999/how-to-determine-file-function-and-line-number
    """
    logger = logging.getLogger()

    # Filename where the function is called from
    func_filename = inspect.currentframe().f_back.f_code.co_filename

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        callerframerecord = inspect.stack()[1]
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        # Line where the function is called from
        func_lineno = info.lineno

        entering_time = datetime.now()
        logger.info(
            f"{Path(func_filename).name} || {func.__module__} || {func_lineno} || Enter || {func.__name__}")

        try:
            return func(*args, **kwargs)

        except Exception:
            error_msg = f"In {func.__name__}"
            logger.exception(error_msg, exc_info=True)

        finally:
            leaving_time = datetime.now()
            logger.info(
                f"{Path(func_filename).name} || {func.__module__} || {func_lineno} || Leave || {func.__name__} || Elapsed: {leaving_time - entering_time}")

    return wrapper


def main(filename: str, logs_path: Path = PROJECT_ROOT / "logs", test: bool = False, log_config_file: Path = PROJECT_ROOT / "conf" / "logging.conf"):
    """
    Instantiate logger object

    Args:
        filename (str): Log file
        path (Path, optional): Path where the log file is saved. Defaults to PROJECT_ROOT/logs/.
        test (bool): Return filename
        log_config_file (Path, optional): Path contaning the log config file. Defaults to PROJECT_ROOT / "conf" / "logging.conf"

    Returns:
        (logging.getLogger()): Logging object

    References:
        [1] https://realpython.com/python-logging/
    """
    # 1. Create logs directory if it doesn't exist
    make_logs_path(logs_path)

    # 2. Instantiate logger object
    logger = make_logger(log_config_file)

    # 3. Create log file
    format_filename = f"{Path(filename).stem}_{datetime.now().date()}_{datetime.now().time()}.log"
    log_format = logging.Formatter(
        '%(asctime)-16s || %(name)s || %(process)d || %(levelname)s || %(message)s')

    fh = make_handler(format_filename, logs_path, log_format)

    logger.addHandler(fh)

    return logger
