import functools
import inspect
import logging
from datetime import datetime
from pathlib import Path
from typing import Callable


def fun(func: Callable):
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
