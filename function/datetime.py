from datetime import datetime, timedelta
from random import randint

import pytz

UTC = pytz.UTC

def get_brazil_time_now():
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
