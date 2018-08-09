import csv

from xlrd import open_workbook

from utils import BaseClass, auto_converter


class CSVUtils(BaseClass):
    def save_to_csv(self, list_of_dict, output_filepath):
        self.logger.debug('save data to %s' % output_filepath)
        if len(list_of_dict) == 0:
            self.logger.warning('report %s is empty nothing to save' % output_filepath)
            return
        keys = list_of_dict[0].keys()
        with open(output_filepath, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys, lineterminator='\n')
            dict_writer.writeheader()
            dict_writer.writerows(list_of_dict)

    def parse_file_with_default_headers(self, file_path, delimiter=';'):
        self.logger.info('get data from %s file with delimiter %s' % (file_path, delimiter))
        with open(file_path) as csv_file:
            sheet = csv.DictReader(csv_file, delimiter=delimiter)
            work_book = []
            for row in sheet:
                for k, v in row.items():
                    row[k] = auto_converter(v)
                work_book.append(row)
        self.logger.debug('file contain %s' % work_book)
        return work_book


class ExcellUtils(BaseClass):
    def parse_file_with_default_headers(self, file_path):
        self.logger.info('get data from %s file' % file_path)
        book = open_workbook(file_path)
        sheet = book.sheet_by_index(0)
        # read header values into the list
        keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]
        dict_list = []
        for row_index in range(1, sheet.nrows):
            d = {keys[col_index]: sheet.cell(row_index, col_index).value for col_index in range(sheet.ncols)}
            dict_list.append(d)
        self.logger.debug('file contain %s' % dict_list)
        return dict_list
