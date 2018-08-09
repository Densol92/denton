from __future__ import division

import subprocess
from multiprocessing.pool import ThreadPool
from pathlib import Path

from api.geckoboard_api import GeckAPI
from api.mongo_db import MongoDB
from api.psql_db import PsqlDB
from settings import ReportPolicy, ConvertPolicy
from settings.settings import ARGS, GECKO, MONGO, METABASE
from utils.date_utils import convert_result
from utils.path_utils import file_name, root_dir
from utils.path_utils import get_report_files, monthly_reports_dir, weekly_reports_dir, daily_reports_dir


def mongo_report(dataset_id, query, report_policy=None, convert_policy=None):
    if report_policy is None:
        report_policy = ReportPolicy.default()
    if convert_policy is None:
        convert_policy = ConvertPolicy.default()

    result = MongoDB.connect_to(MONGO).select(query)
    converted_result = convert_result(result, convert_policy)
    report_result(dataset_id, converted_result, report_policy)
    return converted_result


def report_result(dataset_id, report, report_policy):
    if report_policy.report_to_gecko:
        GeckAPI.connect_to(GECKO).update_dataset(dataset_id, report)

    if report_policy.report_to_mongo:
        MongoDB.connect_to({}).insert_many(dataset_id, report)

    if report_policy.report_to_postgres:
        PsqlDB.connect_to(METABASE).insert_many(dataset_id, report)


def run_one_report(report_path):
    mode = '--test' if ARGS.test else ''
    return_code, output = subprocess.getstatusoutput(f'python {report_path} {mode}')
    print(f"\n=============== START {file_name(report_path)} REPORT ===================\n")
    print(output)

    return return_code


def run_reports(reports_files_path, thread_count):
    pool = ThreadPool(thread_count)

    results = pool.map_async(run_one_report, reports_files_path)
    pool.close()
    pool.join()

    result_codes = results.get()

    print("\n=============== REPORTS FINISHED ===================\n")
    print(f'Total: {len(result_codes)}')
    print(f'Successful: {result_codes.count(0)}')
    print(f'Failed: {result_codes.count(1)}\n\n')
    if result_codes.count(0) != len(result_codes):
        exit(6)


if __name__ == '__main__':
    if ARGS.report_path is not None:
        reports_file_paths = [root_dir() / Path(ARGS.report_path)]
        run_reports(reports_file_paths, 1)

    if ARGS.monthly:
        reports_file_paths = get_report_files(monthly_reports_dir())
        run_reports(reports_file_paths, ARGS.threads_count)

    if ARGS.weekly:
        reports_file_paths = get_report_files(weekly_reports_dir())
        run_reports(reports_file_paths, ARGS.threads_count)

    if ARGS.daily:
        reports_file_paths = get_report_files(daily_reports_dir())
        run_reports(reports_file_paths, ARGS.threads_count)
