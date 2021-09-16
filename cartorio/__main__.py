import logging
import logging.config
import subprocess
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                    stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8'))

import make


def main(filename: str, logs_path: Path = PROJECT_ROOT / "logs", log_config_file: Path = PROJECT_ROOT / "conf" / "logging.conf"):
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
    make.logs_path(logs_path)

    # 2. Instantiate logger object
    logger = make.logger(log_config_file)

    # 3. Create log file
    format_filename = f"{Path(filename).stem}_{datetime.now().date()}_{datetime.now().time()}.log"
    log_format = logging.Formatter(
        '%(asctime)-16s || %(name)s || %(process)d || %(levelname)s || %(message)s')

    fh = make.handler(format_filename, logs_path, log_format)

    logger.addHandler(fh)

    return logger
