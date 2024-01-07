from datetime import datetime, timedelta
from random import randint

import pytz

UTC = pytz.UTC


def get_brazil_time_now() -> datetime:
    delta = timedelta(hours=3)
    dt = datetime.utcnow()
    dt = replace_tzinfo(dt)
    dt = dt - delta

    return dt


def datetime_to_string(dt: datetime) -> str:
    if isinstance(dt, datetime):
        dt = dt.strftime("%d/%m/%Y %H:%M:%S")
    return dt


def utc_to_brazil_datetime(dt: datetime) -> datetime:
    dt = replace_tzinfo(dt)
    delta = timedelta(hours=3)
    return dt - delta


def add_random_minutes_now(dt: datetime = None) -> datetime:
    if not dt:
        dt = get_brazil_time_now()
    dt = replace_tzinfo(dt)
    minutes = randint(5, 10)
    print(f"Adding {minutes} minutes")

    return dt + timedelta(minutes=minutes)


def replace_tzinfo(dt: datetime) -> datetime:
    return dt.replace(tzinfo=UTC)


def get_last_hour() -> datetime:
    now = datetime.now()
    next_hour = now.replace(microsecond=0, second=0, minute=0)

    return next_hour


def get_midnight_hour(get_yesterday: bool = False) -> datetime:
    now = datetime.now()
    midnight_hour = now.replace(microsecond=0, second=0, minute=0, hour=0)

    if get_yesterday:
        midnight_hour = midnight_hour - timedelta(days=1)

    return midnight_hour
