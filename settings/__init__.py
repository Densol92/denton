from utils.date_utils import today


class ReportPolicy(object):
    def __init__(self, report_to_postgres, report_to_mongo, report_to_gecko):
        self.report_to_postgres = report_to_postgres
        self.report_to_mongo = report_to_mongo
        self.report_to_gecko = report_to_gecko

    @classmethod
    def default(cls):
        return cls(True, False, False)


class ConvertPolicy(object):
    def __init__(self, report_timestamp, convert_map):
        self.report_timestamp = report_timestamp
        self.convert_map = convert_map

    @classmethod
    def default(cls):
        return cls(today(), None)
    
    @classmethod
    def default_with_convert_map(cls, convert_map):
        return cls(today(), convert_map)
