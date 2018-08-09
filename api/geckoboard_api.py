import requests
from requests.auth import HTTPBasicAuth

from utils import get_logger


class GeckAPI(object):
    """https://developer.geckoboard.com/api-reference/curl/"""

    def __init__(self, url, token):
        self.logger = get_logger('geckoboard')

        self.auth = HTTPBasicAuth(token, '')
        self.base_url = url

    def __send_post(self, url, data):
        result = requests.post(url, json=data, auth=self.auth)
        self.logger.debug(result.content)
        assert result.status_code in (200, 201), result.content
        return result

    def __send_delete(self, url):
        result = requests.delete(url, auth=self.auth)
        self.logger.debug(result.content)
        assert result.status_code in (200, 201), result.content
        return result

    def __send_put(self, url, data):
        result = requests.put(url, json=data, auth=self.auth)
        self.logger.debug(result.content)
        assert result.status_code in (200, 201), result.content
        return result

    def replace_all_data_in_dataset(self, dataset_id, data):
        self.logger.info('replace all data in dataset %s' % dataset_id)
        url = '%s%s/data' % (self.base_url, dataset_id)
        body = {'data': data}
        return self.__send_put(url, body)

    def update_dataset(self, dataset_id, data):
        if self.base_url is None:
            self.logger.info("TEST update dataset %s" % dataset_id)
            return

        self.logger.info('update dataset %s' % dataset_id)
        url = '%s%s/data' % (self.base_url, dataset_id)
        body = {'data': data}
        return self.__send_post(url, body)

    # https://developer.geckoboard.com/#find-or-create-a-new-dataset
    def find_or_create_dataset(self, dataset_id, dataset_structure, unique_by=None):
        if self.base_url is None:
            self.logger.info("TEST find_or_create_dataset %s" % dataset_id)
            return

        self.logger.info('create new dataset %s' % dataset_id)
        url = self.base_url + dataset_id
        body = {'fields': dataset_structure}
        if unique_by:
            body.update({'unique_by': unique_by})
        return self.__send_put(url, body).json()

    def delete_dataset(self, dataset_id):
        self.logger.info('delete dataset %s' % dataset_id)
        url = self.base_url + dataset_id
        return self.__send_delete(url)

    @classmethod
    def connect_to(cls, gecko_config):
        return cls(**gecko_config)
