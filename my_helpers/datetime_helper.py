import datetime
import pytz


DEFAULT_TIMEZONE = 'Asia/Kolkata'

DATE_FORMAT = "%d/%m/%Y"
TIME_FORMAT = "%I:%M %p"
TIME_24_FORMAT = "%H:%M:%S"

DATE_TIME_FORMAT = "{} {}".format(DATE_FORMAT, TIME_FORMAT)


def string_to_date(start_date):
    """
    to convert date string to date object
    @:param: date string
    """
    if start_date and start_date != "":

        try:
            s_date = datetime.datetime.strptime(start_date, DATE_FORMAT).date()
        except Exception as error:
            print('error: ',error)
            s_date = start_date
        return s_date
    else:
        return None


def date_to_string(date):
    """
    to convert date object to date string
    @:param: date object
    """
    if date:
        try:
            date = date.strftime(DATE_FORMAT)
        except ValueError:
            date = date
    return date



def string_to_time(c_time, timezone):
    """
    to convert time string to time object
    @:param: time string
    """
    if c_time:

        try:
            date = datetime.datetime.strptime(c_time, TIME_FORMAT)
            if timezone:
                utc = pytz.utc
                local_timezone = pytz.timezone(timezone)
                local_date = local_timezone.localize(date)
                date = local_date.astimezone(utc)
            c_time = date.time()

        except Exception as error:
            print("==> string_to_time Exception error:", error)
            pass
    
    return c_time



def time_to_string(c_time, timezone=None):
    """
    to convert time object to time string
    @:param: time object
    """
    if c_time:
        try:
            start_time = datetime.datetime.strftime(c_time, TIME_FORMAT)
            return start_time
        except Exception as error:
            print('error: ', error)
            return c_time


def string_to_date_time(date, timezone=None):
    """
    to convert string date format to datetime object
    @:param: date(in string format), timezone
    """
    if date:
        try:
            date = datetime.datetime.strptime(date, DATE_TIME_FORMAT)
            if timezone:
                utc = pytz.utc
                local_timezone = pytz.timezone(timezone)
                local_date = local_timezone.localize(date)
                date = local_date.astimezone(utc)
                print("==> date:", date)
        except Exception as error:
            print("==> string_to_date_time Exception error:", error)
            pass

    return date



def datetime_to_string(date, company_timezone=None):
    """
    to convert datetime to  string date format object
    @:param: datetime object, timezone
    """
    
    if date:
        try:
            if company_timezone:

                if date.tzinfo is None or date.tzinfo.utcoffset(date) is None:
                    calculative_date = pytz.utc.localize(date)
                    date = calculative_date.astimezone(pytz.timezone(company_timezone))

                date = date.astimezone(pytz.timezone(company_timezone))
            date = date.strftime(DATE_TIME_FORMAT)
        except Exception as error:
            date = date.strftime(DATE_TIME_FORMAT)
            print("==> Exception error: ", error)
            date = date
    return date



def apply_my_timezone(date_time, my_timezone=None):
    """
    to apply timezone on datetime
    @:param: datetime object, timezone
    """

    import pytz
    if my_timezone:
        utc = pytz.utc
        local_timezone = pytz.timezone(my_timezone)
        local_date = local_timezone.localize(date_time)
        date_time = local_date.astimezone(utc)
        if date_time:
            date_time = date_time.astimezone(pytz.timezone(my_timezone))
    return date_time


def timestamp_to_datetime(timestamp):
    from datetime import datetime
    # timestamp = 1545730073
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object


def datetime_to_timestamp(dt_object):
    # current date and time
    # ndt_objectow = datetime.now()
    if dt_object:
        from datetime import timezone

        timestamp = dt_object.replace(tzinfo=timezone.utc).timestamp()
        return timestamp
    else:
        return  None
