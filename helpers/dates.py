from datetime import datetime, timedelta
import pytz
from dateutil.relativedelta import relativedelta
import math


def quarter_range(date=None):
    if date is None:
        date = current_datetime_jkt()
    current_quarter = math.floor((date.month - 1) / 3 + 1)
    first_date = datetime(date.year, 3 * current_quarter - 2, 1)
    last_date = datetime(date.year, 3 * current_quarter, 1) + relativedelta(months=1) + timedelta(days=-1)

    return first_date, last_date


def current_datetime_sgp(timezone='Asia/Singapore'):

    return datetime.now(pytz.timezone(timezone))


def current_datetime_jkt(timezone='Asia/Jakarta'):

    return datetime.now(pytz.timezone(timezone))