import sys
import subprocess
import warnings
from pathlib import Path

import pytest
from structlog.testing import capture_logs

PROJECT_ROOT = Path(subprocess.Popen(
    ['git', 'rev-parse', '--show-toplevel'],
    stdout=subprocess.PIPE
).communicate()[0].rstrip().decode('utf-8'))

sys.path.insert(0, str(PROJECT_ROOT))

from cartorio.log import make_logger, log, _configure_structlog


def test_make_logger_returns_tuple():
    """make_logger returns a (logger, timestamp_str) two-tuple."""
    result = make_logger("test")
    assert isinstance(result, tuple)
    assert len(result) == 2
    _, ts = result
    assert isinstance(ts, str) and ts


def test_make_logger_bound_logger():
    """The logger returned by make_logger has standard log-level methods."""
    logger, _ = make_logger("test")
    for method in ("info", "debug", "warning", "error", "exception"):
        assert callable(getattr(logger, method, None)), f"missing method: {method}"


def test_logs_path_deprecation_warning():
    """Passing logs_path emits a DeprecationWarning."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        make_logger("test", logs_path=Path("/tmp"))
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)


def test_fun():
    """log decorator propagates return values and re-raises exceptions."""
    @log
    def divide(num1, num2):
        return num1 / num2

    @log
    def multiply(num1, num2):
        return num1 * num2

    assert multiply(10, 2) == 20

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_log_decorator_emits_enter_leave():
    """log decorator emits enter and leave events with required keys."""
    @log
    def add(a, b):
        return a + b

    with capture_logs() as cap:
        add(1, 2)

    events = [e["event"] for e in cap]
    assert "enter" in events
    assert "leave" in events

    leave = next(e for e in cap if e["event"] == "leave")
    assert "function" in leave
    assert "elapsed" in leave


def test_log_decorator_captures_exception():
    """log decorator emits an error event when the wrapped function raises."""
    @log
    def boom():
        raise ValueError("test error")

    with capture_logs() as cap:
        with pytest.raises(ValueError):
            boom()

    events = [e["event"] for e in cap]
    assert "error" in events


def test_configure_structlog_force():
    """_configure_structlog(force=True) re-runs without error."""
    _configure_structlog(force=True)
    _configure_structlog(force=True)
