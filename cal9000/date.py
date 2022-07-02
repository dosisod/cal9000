from datetime import datetime


def get_today_date_only() -> datetime:
    """
    We have to do this hack because there is no easy way do get just the
    "date" portion of a datetime object, and still have it be a datetime.
    """
    return datetime.fromtimestamp(float(datetime.now().date().strftime("%s")))
