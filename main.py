from make_logger import log_fun, make_logger
import logging
from datetime import datetime

logger = make_logger()

@log_fun
def divide(num1, num2):
    return num1 / num2


if __name__ == '__main__':

    logger.debug("Hey")

    result = divide(10, 0)
    print(result)