import logging
import logging.config
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                    stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8'))
                    

def logs_path(path: Path = PROJECT_ROOT / "logs") -> Path:
    """
    Create logs directory if it doesn't exist

    Args:
        path (Path, optional): Path where the log file is saved. Defaults to PROJECT_ROOT/logs/.
        test (bool): Return filename

    Returns:
        (Path): Path to logs directory

    Example:
        >>> _ = make_logs_path()
    """
    path.mkdir(parents=True, exist_ok=True)

    return


def logger(log_config_file: Path = PROJECT_ROOT / "cartorio" / "conf" / "logging.conf"):

    logging.config.fileConfig(str(log_config_file),
                              disable_existing_loggers=False)

    return logging.getLogger()


def handler(filename: str, logs_path: Path, log_format: str):

    fh = logging.FileHandler(str(logs_path / f'{filename}'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_format)

    return fh
