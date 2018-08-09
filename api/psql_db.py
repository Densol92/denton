from datetime import datetime

import dataset

from utils import BaseClass


class PsqlDB(BaseClass):
    def __init__(self, host, db_name, user, password=None, schema=None, port=None):
        super(PsqlDB, self).__init__()
        password = '' if password is None else password
        port = '5432' if port is None else port

        uri = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        self.db = dataset.connect(uri, schema)

    def execute_sql(self, sql):
        self.logger.debug('execute sql: %s with params %s' % (sql, None))
        result = self.db.query(sql)
        return [row for row in result]

    def insert_many(self, report_name, report, date_=None):
        if len(report) == 0:
            self.logger.info('nothing to insert')
            return

        self.logger.info('Insert %s row to table %s' % (len(report), report_name))
        # todo remove date insert in low level methods
        if date_ is None:
            date_ = datetime.today()
        for row in report:
            row['date'] = date_
        self.db.get_table(report_name).insert_many(report)

    @classmethod
    def connect_to(cls, db_conf):
        return cls(**db_conf)
