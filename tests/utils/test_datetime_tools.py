import datetime

from utils.datetime_tools import TIMEZONE, seven_days_before


def test_seven_days_before_datetime() -> None:
    now = datetime.datetime.now(tz=TIMEZONE)
    before = seven_days_before(now)
    assert before == now - datetime.timedelta(days=7)


def test_seven_days_before_int() -> None:
    now = datetime.datetime.now(tz=TIMEZONE).replace(microsecond=0)  # now() includes useless us
    now_epoch = int(now.timestamp())
    before = seven_days_before(now_epoch)
    assert before == int((now - datetime.timedelta(days=7)).timestamp())


def test_seven_days_before_none() -> None:
    before_default_value = datetime.datetime.now(tz=TIMEZONE) - datetime.timedelta(days=7)
    default_value = seven_days_before()
    after_default_value = datetime.datetime.now(tz=TIMEZONE)
    assert before_default_value < default_value < after_default_value
