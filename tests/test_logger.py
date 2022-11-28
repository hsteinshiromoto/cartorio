import logging
import subprocess
import sys
from pathlib import Path

import pytest
import tempfile

PROJECT_ROOT = Path(subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                    stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8'))

sys.path.append(str(PROJECT_ROOT))

from cartorio.log import *


def test_make_logs_path():
    """Test if folder is created
    """

    path = Path(tempfile.mkdtemp())
    make_path(path)
    
    assert path.is_dir()


def test_set_handler():
    """Test if file handler is set
    """
    
    path = Path(tempfile.mkdtemp())
    make_path(path)

    format_filename = f"{Path(__file__).stem}.log"
    log_format = logging.Formatter('%(asctime)-16s || %(name)s || %(process)d || %(levelname)s || %(message)s')
    handler = set_handler(format_filename, log_format, path)

    # Test handler data type
    assert isinstance(handler, logging.FileHandler)

    # Test if file handler basename is correct
    msg = f"Expected baseFilename to be {handler.baseFilename}. Got {path / f'{Path(__file__).stem}.log'}."
    assert handler.baseFilename == str(path / format_filename), msg

    # Test if file handler level is correct
    assert handler.level == 10

    # Test if log file has been generated
    assert Path(handler.baseFilename).is_file() == True


def test_fun():
    """Test log function
    """
    @log
    def divide(num1, num2):
        return num1 / num2

    @log
    def multiply(num1, num2):
        return num1 * num2

    # Test if entry and exit log messages are correct
    multiply(10, 1)

    # Test if raised error is correct
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_log():
    """Test main function
    """
    logs_path = Path(tempfile.mkdtemp())
    logger, _ = make_logger("test.log", logs_path)
    
    assert True