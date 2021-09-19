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
        assert Path(handler.baseFilename).is_file() == True


def test_fun():
    @fun
    def divide(num1, num2):
        return num1 / num2

    @fun
    def multiply(num1, num2):
        return num1 * num2

    multiply(10, 1)

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_log():
    logs_path = Path(tempfile.mkdtemp())
    logger = log("test.log", logs_path)
    
    assert True