from __future__ import division
import logging
import sys

import os
from mailer import Mailer
from mailer import Message

DEFAULT_LOGGER = 'report'
GECKOBOARD_DATE_FORMAT = '%Y-%m-%d'
MONTHLY_REPORT_NAME_FORMAT = '%Y%m%d'
FILE_DATETIME_FORMAT = "%Y-%m-%d_%H_%M_%S"


class BaseClass(object):
    def __init__(self, logger=None):
        self.logger = logger
        if logger is None:
            self.logger = get_logger()


def get_logger(name=DEFAULT_LOGGER, log_path=None, logging_level=logging.INFO):
    """it remember only first log path """
    if logging.getLogger(name).handlers:
        return logging.getLogger(name)

    logger_format = "[%(asctime)s] %(levelname)s %(message)s"
    logging.basicConfig(stream=sys.stdout, level=logging_level, format=logger_format)

    _logger = logging.getLogger(name)

    if log_path is not None:
        logs_folder = os.path.split(log_path)[0]
        if not os.path.exists(logs_folder):
            os.makedirs(logs_folder)

        _logger_file_handler = logging.FileHandler(log_path)
        _logger_file_handler.setFormatter(logging.Formatter(logger_format))
        _logger.addHandler(_logger_file_handler)
    else:
        pass
        # _logger.warn('for logger "%s" path to logfile not defined' % name)
    return _logger


def auto_converter(s):
    """automaticaly convert string to the int or float"""
    for fn in int, float:
        try:
            return fn(s)
        except ValueError:
            pass
    return s


def send_email(sender=REPORT_SENDER, recipient=REPORT_RECIPIENTS, subject='Reports finished', body=None):
    try:
        message = Message(From=sender, To=recipient, Subject=subject)
        message.Body = body

        sender = Mailer(EMAIL_RELAY)
        sender.send(message)
    except Exception as e:
        get_logger().error(e)


def calculate_nps(rate):
    """
    Calculate NPS - https://en.wikipedia.org/wiki/Net_Promoter
    :param rate: structure like  [{"rate": 8, "total": 12},{"rate": 9, "total": 22}]
    where rate is NPS score and total - number of votes
    :return:
    """
    good_rates, bad_rates, total = calculate_rates(rate)
    return (good_rates - bad_rates) / total


def calculate_rates(rate):
    total = sum(map(lambda x: x['total'], rate))
    good = sum(map(lambda x: x['total'], filter(lambda x: x['rate'] > 8, rate)))
    bad = sum(map(lambda x: x['total'], filter(lambda x: x['rate'] < 7, rate)))
    return good, bad, total
