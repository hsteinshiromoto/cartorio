import functools
import inspect
import os
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Tuple

import structlog

_STRUCTLOG_CONFIGURED = False


def _configure_structlog(force: bool = False) -> None:
    """Configure structlog processors chain.

    Reads the LOG_FORMAT environment variable to select output format:
    - ``LOG_FORMAT=json``: one JSON object per log line (production).
    - anything else (or absent): coloured console output (development).

    Args:
        force: Re-configure even if already configured. Useful in tests
            when LOG_FORMAT changes between test cases.

    Example:
        >>> _configure_structlog()
        >>> _configure_structlog(force=True)  # reset, e.g. in tests
    """
    global _STRUCTLOG_CONFIGURED
    if _STRUCTLOG_CONFIGURED and not force:
        return

    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.ExceptionRenderer(),
    ]

    log_format = os.getenv("LOG_FORMAT", "console").lower()
    if log_format == "json":
        final_processor = structlog.processors.JSONRenderer()
    else:
        final_processor = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [final_processor],
        wrapper_class=structlog.make_filtering_bound_logger(0),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    _STRUCTLOG_CONFIGURED = True


def make_logger(
    filename: Any,
    logs_path: Optional[Path] = None,
    **kwargs: Any,
) -> Tuple[Any, str]:
    """Return a structlog bound logger and a timestamp string.

    Accepts the same positional signature as the previous ``logging``-based
    implementation so existing callers that do ``logger, _ = make_logger(...)``
    continue to work without changes.

    Args:
        filename: Source file or logical name used to derive the logger name.
            Typically ``__file__`` or a plain string such as ``"myapp"``.
        logs_path: Accepted but ignored. File-based logging is no longer
            supported.  Passing a non-``None`` value emits a
            ``DeprecationWarning``.
        **kwargs: Additional keyword arguments are accepted but ignored for
            backwards compatibility.

    Returns:
        A two-element tuple ``(bound_logger, timestamp)`` where
        ``bound_logger`` is a :class:`structlog.BoundLogger` instance and
        ``timestamp`` is an ISO-like string (``"%Y-%m-%d_%H-%M-%S"``).

    Example:
        >>> logger, ts = make_logger("myapp")
        >>> logger.info("hello", key="value")
    """
    if logs_path is not None:
        warnings.warn(
            "logs_path is ignored; file-based logging is no longer supported.",
            DeprecationWarning,
            stacklevel=2,
        )

    _configure_structlog()
    name = Path(filename).stem if filename else "cartorio"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return structlog.get_logger(name), timestamp


def log(func):
    """Decorator that logs entry, exit, elapsed time, and exceptions.

    Uses structlog to emit structured events:

    * ``event="enter"`` — emitted before the function executes.
    * ``event="leave"`` — emitted after the function returns (or raises).
    * ``event="error"`` — emitted when an unhandled exception is raised.

    Each event carries ``function``, ``module``, ``filename``, and (for
    ``"leave"`` and ``"error"``) ``elapsed`` keys.

    Args:
        func: The callable to wrap.

    Returns:
        The wrapped callable with identical signature.

    Example:
        >>> @log
        ... def add(a, b):
        ...     return a + b
        >>> add(1, 2)
        3
    """
    _configure_structlog()
    logger = structlog.get_logger(func.__module__)
    _frame = inspect.currentframe()
    func_filename = _frame.f_back.f_code.co_filename if _frame and _frame.f_back else __file__

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        entering_time = datetime.now()
        logger.info(
            "enter",
            function=func.__name__,
            module=func.__module__,
            filename=Path(func_filename).name,
        )
        try:
            result = func(*args, **kwargs)
        except Exception:
            elapsed = str(datetime.now() - entering_time)
            logger.exception(
                "error",
                function=func.__name__,
                module=func.__module__,
                elapsed=elapsed,
            )
            raise
        else:
            elapsed = str(datetime.now() - entering_time)
            logger.info(
                "leave",
                function=func.__name__,
                module=func.__module__,
                elapsed=elapsed,
            )
            return result

    return wrapper
