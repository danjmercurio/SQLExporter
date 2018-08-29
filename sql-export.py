#!/usr/bin/python

import datetime
try:
    from dateutil import parser
except ImportError:
    raise SystemExit("dateutil module not found. \
                     Run pip install python-dateutil")


# Define the exporter as a class so we can reuse it other scripts and contexts
class SQLExporter(object):

    def __init__(self, dbdriver='mysql', host='localhost', password=None,
                 db=None, output_filename='output.csv'):
        self.host = host
        self.password = password
        self.db = db
        self.output_filename = output_filename

        ''' Define the delimiters we will use; Following is from spec:
            Comma: Field break indicator, default is (ASCII 20), customizable,
            avoid characters in data
            Quote: Keeps text together, default is  (ACSII 254) and is only
            required around fields that have text and spaces, customizable,
            avoid characters in data
            Newline: Manual line break and text wraps within a field, default
            is  (ASCII 174), customizable, avoid characters in data
            New Record: Starts a new record, final carriage return loads the
            last record, cannot be changed, industry standard
        '''
        self.delimiters = {
            'COMMA': ",",
            'QUOTE': "\"",
            'NEWLINE': "\n",
            'NEWRECORD': "\r\n"
        }
        self.DATE_FORMAT = "%Y/%m/%d"

    def __doc__(self):
        return \
            ''' Export SQL according to some arbitrary rules,
                with arbitrary delimiters for the output,
                which are specified here=
                https=//help.lexisnexis.com/litigation/ac/cn_classic/managing_data_files.htm
            '''

    def normalize_date(self, date):
        '''
        The spec included a format for dates:
        Date fields are an 8-character maximum with slashes.
        If dates include slashes, you can import any format.
        If slashes are not used, then you must use the universal
        date format of YYYYMMDD or the mm-dd-yyyy date format with dashes.
        '''

        types = {
            str: (lambda: parser.parse(date).strftime(self.DATE_FORMAT)),
            int: (lambda: datetime.date.fromtimestamp(date).strftime(self.DATE_FORMAT)),
            float: (lambda: datetime.date.fromtimestamp(date).strftime(self.DATE_FORMAT)),
            datetime.date: (lambda: date.strftime(self.DATE_FORMAT))
        }

        return types[type(date)]()

    def export(self):
        pass


if (__name__ == "__main__"):
    s = SQLExporter()
    print s.normalize_date("04.02.1992")
    print s.normalize_date(1535516087)
    print s.normalize_date(1535516087.322354)
    print s.normalize_date(datetime.date.today())
