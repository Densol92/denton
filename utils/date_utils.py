import time
from datetime import datetime

from dateutil.relativedelta import relativedelta

from settings.settings import GECKOBOARD_DATE_FORMAT, FILE_DATETIME_FORMAT
from utils import *


def now():
    return datetime.now().strftime(FILE_DATETIME_FORMAT)


def today(date_format=GECKOBOARD_DATE_FORMAT):
    return datetime.today().strftime(date_format)


def first_day_of_month(date_format=GECKOBOARD_DATE_FORMAT, shift_month=0):
    first_day_of_month_date = datetime.today().replace(day=1) - relativedelta(months=shift_month)
    return first_day_of_month_date.strftime(date_format)


def previous_monday():
    return (datetime.today() - relativedelta(weekday=0, weeks=2)).date()


def get_month_number(shift=0):
    n_month_ago = datetime.today() - relativedelta(months=shift)
    date_string = n_month_ago.strftime("%Y-%m")
    return date_string


def timeit(method):
    def timed(*args, **kw):
        time_start = time.time()
        result = method(*args, **kw)
        time_end = time.time()
        try:
            self_ = args[0]
            # class must contain logger instance
            self_.logger.info('method %s.%s take %s second to finished' % (type(self_).__name__, method.__name__, time_end - time_start))
        except Exception as e:
            print(e)
        return result

    return timed


def convert_result(result, convert_policy):
    logger = get_logger()
    result_list = []

    for row in result:
        elem = {}

        if convert_policy.convert_map is not None:
            for key, value in row.items():
                if convert_policy.convert_map[key] is not None:
                    elem.update({convert_policy.convert_map[key]: value})
        else:
            elem = row

        if convert_policy.report_timestamp is not None:
            elem['date'] = convert_policy.report_timestamp

        result_list.append(elem)

    logger.debug('data %s after converting with map %s is %s' % (result, convert_policy.convert_map, result_list))
    return result_list
