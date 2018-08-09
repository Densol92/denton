from argparse import ArgumentParser

import yaml

from utils.path_utils import config_file_path


def get_config(test_mode):
    return yaml.load(open(config_file_path(test_mode), 'r'))


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
CONFIG = get_config(ARGS.test)

DEBUG = CONFIG.get('debug', True)
