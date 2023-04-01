from __future__ import annotations

from datetime import datetime, tzinfo
import pytz


TIMEZONE = pytz.timezone("Europe/Zurich")


class Datetime:
    """A class for datetime related functionality."""

    @classmethod
    def get_local_datetime(cls, timezone: tzinfo = TIMEZONE) -> datetime:
        if not isinstance(timezone, tzinfo):
            raise TypeError(f"timezone must be of type tzinfo not {timezone.__class__.__name__}")

        utc = datetime.now()
        local_dt = utc.astimezone(timezone)

        return local_dt
