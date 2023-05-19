from datetime import datetime, timedelta
from random import randint


def get_brazil_time_now():
    delta = timedelta(hours=3)
    dt = datetime.utcnow() - delta
    return dt


def datetime_to_string(dt: datetime) -> str:
    if isinstance(dt, datetime):
        dt = dt.strftime("%d/%m/%Y %H:%M:%S")
    return dt


def add_random_minutes_now() -> datetime:
    minutes = randint(5, 10)
    print(f"Adding {minutes} minutes")

    return get_brazil_time_now() + timedelta(minutes=minutes)
