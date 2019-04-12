import datetime
import time
import pytz


def convert_datetime_str_to_timestamp(datetime_str, tz):
    if ':' in datetime_str and tz:
        datetime_str = datetime_str + tz
        date_format = "%d.%m.%Y %H:%M:%S%z" if datetime_str.count(':') == 2 else "%d.%m.%Y %H:%M%z"
    elif ':' in datetime_str and not tz:
        date_format = "%d.%m.%Y %H:%M:%S" if datetime_str.count(':') == 2 else "%d.%m.%Y %H:%M"
    elif tz:
        datetime_str = datetime_str + tz
        date_format = "%d.%m.%Y%z"
    elif not tz:
        date_format = "%d.%m.%Y"

    if tz:
        return int(
            datetime.datetime.strptime(datetime_str, date_format).astimezone(pytz.utc).timestamp()) * 1000
    else:
        return int(
            (datetime.datetime.strptime(datetime_str, date_format) - datetime.datetime(1970, 1,
                                                                                       1)).total_seconds()
            * 1000
        )

def get_utc():
    return int(time.time()) * 1000