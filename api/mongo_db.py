from pymongo.mongo_client import MongoClient

from utils import get_logger
from utils.date_utils import timeit


class MongoDB(object):
    def __init__(self, host, db_name, collection, user=None, password=None, port=None):
        self.logger = get_logger('mongo_db')
        port = 27017 if port is None else port

        connection = MongoClient(host, port)
        db = connection[db_name]
        if user is not None:
            db.authenticate(user, password)
        self.collection = db[collection]

    @timeit
    def aggregate(self, pipe):
        self.logger.info('get data from mongo')
        result = self.collection.aggregate(pipeline=pipe, allowDiskUse=True)
        result_list = []
        for document in result:
            result_list.append(document)
        self.logger.debug('result of %s is %s' % (pipe, result_list))
        return result_list

    @classmethod
    def connect_to(cls, db_conf):
        return cls(**db_conf)
