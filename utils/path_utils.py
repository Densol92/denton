import os
from pathlib import Path


def root_dir():
    return Path(__file__).parent.parent


def daily_reports_dir():
    return root_dir() / "daily_reports"


def weekly_reports_dir():
    return root_dir() / "weekly_reports"


def monthly_reports_dir():
    return root_dir() / "monthly_reports"


def config_file_path():
    return root_dir() / "settings" / "config.yml"


def file_name(file_path):
    return Path(file_path).name


def get_report_files(report_directory):
    reports_files_paths = []
    for root, sub_dirs, files in os.walk(report_directory):
        for file_name_ in files:
            if '__init__' not in file_name_ and '.py' in file_name_:
                reports_files_paths.append(os.path.join(root, file_name_))

    return reports_files_paths
