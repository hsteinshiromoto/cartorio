import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest
import tempfile

PROJECT_ROOT = Path(subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                    stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8'))

sys.path.append(str(PROJECT_ROOT))

from cartorio.log import *

# LOGGER, FILENAME = make_logger(__file__, test=True)

def test_make_logs_path():

    path = Path(tempfile.mkdtemp())
    make_path(path)
    
    assert path.is_dir()


def test_set_handler():
    
        path = Path(tempfile.mkdtemp())
        make_path(path)
    
        format_filename = f"{Path(__file__).stem}.log"
        log_format = logging.Formatter('%(asctime)-16s || %(name)s || %(process)d || %(levelname)s || %(message)s')
        handler = set_handler(format_filename, log_format, path)
    
        assert isinstance(handler, logging.FileHandler)
        msg = f"Expected baseFilename to be {handler.baseFilename}. Got {path / f'{Path(__file__).stem}.log'}."
        assert handler.baseFilename == str(path / format_filename), msg
        assert handler.level == 10

# @log_fun
# def divide(num1, num2):
#     return num1 / num2


# @log_fun
# def multiply(num1, num2):
#     return num1 * num2


# def test_logfile():
#     assert Path(FILENAME).is_file() == True


# if __name__ == '__main__':

#     result = divide(10, 0)

#     LOGGER.info("Again")

#     result = multiply(10, 1)
