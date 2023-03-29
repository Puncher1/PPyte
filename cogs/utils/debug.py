import sys

import inspect
from enum import Enum

from .dt import Datetime
from .common import MISSING


class _Formatter:
    INFO = "\x1b[34;1m"
    WARNING = "\x1b[33;1m"
    ERROR = "\x1b[31;1m"
    CRITICAL = "\x1b[41;1m"

    PURPLE = "\x1b[35m"
    GREEN = "\x1b[32m"
    BLUE = "\x1b[34m"

    BOLD = "\x1b[1m"
    RST = "\x1b[0m"


class LogLevel(Enum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


level_colors = {
    LogLevel.info: _Formatter.INFO,
    LogLevel.warning: _Formatter.WARNING,
    LogLevel.error: _Formatter.ERROR,
    LogLevel.critical: _Formatter.CRITICAL,
}


def log(msg: str, *, level: LogLevel, context: str = MISSING):
    """To print a debug information onto the console."""
    f = _Formatter

    if not isinstance(level, LogLevel):
        raise TypeError(f"level must be of type LogLevel not {level.__class__.__name__}")

    level_fm = "%-*s" % (8, level.value)

    if context is not MISSING:
        if not isinstance(context, str):
            raise TypeError("context must be a str")

        context_fm = f"{f.BLUE}{context} "
    else:
        context_fm = ""

    dt_format = "%Y-%m-%d %H:%M:%S"
    dt = Datetime.get_local_datetime().strftime(dt_format)

    frame = inspect.stack()[1]
    caller = inspect.getframeinfo(frame[0])
    filename = caller.filename.split("\\")[-1]

    print(
        f"{f.BOLD}{dt} {level_colors[level]}{level_fm}{f.RST} {f.PURPLE}Punchax:{filename} {context_fm}{f.RST}{msg}",
        file=sys.stderr,
    )
