from io import TextIOWrapper
from random import randint
from zipfile import ZipFile

import requests
from requests.auth import HTTPBasicAuth


def download_file_from_url(file_url, credentials=None):
    local_file_path = 'report_%s_%s' % (randint(100000, 1000000), file_url.split('/')[-1])
    local_file_path = local_file_path.replace(' ', '_')
    auth = None
    if credentials:
        auth = HTTPBasicAuth(*credentials)
    r = requests.get(file_url, stream=True, auth=auth)

    # todo use temp file
    with open(local_file_path, 'wb+') as downloaded_storage_file:
        downloaded_storage_file.write(r.content)
        downloaded_storage_file.flush()
    return local_file_path


def extract_file_from_zip(file_path):
    report = ZipFile(file_path)
    extracted_report_file = report.open(report.namelist()[0], 'r')
    # csv dictReader doesn't support default zip encoding so we need to convert it in right format
    extracted_report_file = TextIOWrapper(extracted_report_file, encoding='utf_8_sig')
    return extracted_report_file
