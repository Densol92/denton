from argparse import ArgumentParser

import yaml

from utils.path_utils import config_file_path


def get_config():
    return yaml.load(open(config_file_path(), 'r'))


def get_cli_arguments():
    parser = ArgumentParser(description='Run reports')
    parser.add_argument('--monthly', action='store_true')
    parser.add_argument('--weekly', action='store_true')
    parser.add_argument('--daily', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--threads', dest='threads_count', type=int, default=10)
    parser.add_argument("report_path", nargs='?', default=None)
    args = parser.parse_args()
    return args


ARGS = get_cli_arguments()
CONFIG = get_config()

DEBUG = CONFIG.get('debug', True)

GECKO = CONFIG.get('geckoboard')
MONGO = CONFIG.get('mongo')
METABASE = CONFIG.get('metabase')

email = CONFIG.get('email', {})
EMAIL_RELAY = email.get('relay', 'wrong_relay.host.com')
REPORT_RECIPIENTS = email.get('recipients', [])
REPORT_SENDER = email.get('from', 'a@b.c')
