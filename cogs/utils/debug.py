import sys

import inspect
from enum import Enum

from .dt import Datetime


class _Formatter:
    INFO = "\x1b[34;1m"
    WARNING = "\x1b[33;1m"
    ERROR = "\x1b[31;1m"
    CRITICAL = "\x1b[41;1m"

    PURPLE = "\x1b[35m"
    GREEN = "\x1b[32m"

    BOLD = "\x1b[1m"
    RST = "\x1b[0m"


class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


level_colors = {
    LogLevel.INFO.value: _Formatter.INFO,
    LogLevel.WARNING.value: _Formatter.WARNING,
    LogLevel.ERROR.value: _Formatter.ERROR,
    LogLevel.CRITICAL.value: _Formatter.CRITICAL,
}


def log(msg: str, *, level: LogLevel):
    f = _Formatter

    dt_format = "%Y-%m-%d %H:%M:%S"
    dt = Datetime.get_local_datetime().strftime(dt_format)

    level = level.value
    level_fm = "%-*s" % (8, level)

    frame = inspect.stack()[1]
    caller = inspect.getframeinfo(frame[0])
    filename = caller.filename.split("\\")[-1]

    print(f"{f.BOLD}{dt} {level_colors[level]}{level_fm}{f.RST} {f.PURPLE}PPyte:{filename} {f.RST}{msg}", file=sys.stderr)  # type: ignore
