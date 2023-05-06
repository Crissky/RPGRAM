from datetime import datetime, timedelta


def get_brazil_time_now():
    delta = timedelta(hours=3)
    dt = datetime.utcnow() - delta
    return dt


def datetime_to_string(dt: datetime) -> str:
    if isinstance(dt, datetime):
        dt = dt.strftime("%d/%m/%Y %H:%M:%S")
    return dt