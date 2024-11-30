import datetime

from plum import dispatch

TIMEZONE = datetime.UTC


@dispatch
def seven_days_before(date: datetime.datetime | None = None) -> datetime.datetime:
    if date is None:
        date = datetime.datetime.now(tz=TIMEZONE)
    elif not isinstance(date, datetime.datetime):
        raise TypeError
    return date - datetime.timedelta(days=7)


@dispatch
def seven_days_before(date: int) -> int:  # noqa: F811
    before: datetime.datetime = datetime.datetime.fromtimestamp(date) - datetime.timedelta(days=7)  # noqa: DTZ006
    return int(before.timestamp())
