from datetime import datetime, timedelta


def get_brazil_time_now():
    delta = timedelta(hours=3)
    dt = datetime.utcnow() - delta
    return dt
