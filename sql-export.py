#!/usr/bin/python


# Define the exporter as a class so we can reuse it other scripts and contexts


class SQLExporter(object):

    def __init__(self, dbdriver='mysql', host='localhost', password=None,
                 db=None, output_filename='output.csv', logging=None, logger_output=None):
        self.host = host
        self.password = password
        self.db = db
        self.output_filename = output_filename
        try:
            import importlib
        except ImportError:
            raise SystemExit('''You are using an out of date version of Python.
                             This utility requires Python 2.7.x or later')''')
        self.deps = dict()  # Module dependencies
        for module in ['sys', 'datetime', 'dateutil', 'pyodbc', 'logging']:
            try:
                self.deps[module] = importlib.import_module(module)
            except ImportError as e:
                modname = e.args[0].split(' ')[-1]
                raise SystemExit("""Dependent module \"{0}\" not found.
Run pip install {0} or sudo apt-get install python-{0}, or install the module another way.""".format(modname))
        self.logging = logging
        self.logger_output = logger_output
        if self.logging:
            self.deps.get('logging').basicConfig(filename=self.logger_output)
            self.logger = self.deps.get('logging').getLogger()
            self.logger.info('PySqlExport 1.0')
            self.logger.info('Started with logging enabled. Logfile is set to {0}'.format(self.logger_output))
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

    def connect_db(self):
        ''' Define methods to connect to various SQL implementations
            and then connect, returning a database cursor
        '''
        def connect_mysql():
            pass

        def connect_ms():
            pass

        def connect_sqlite():
            import sqlite3
            sqlite3.connect(self.database, timeout=None, isolation_level=None, detect_types=None, factory=None)

        drivers = {
            "mysql": connect_mysql,
            "sqlite": connect_sqlite,
            "mssql": connect_ms
        }.get(self.driver)()

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
        return {
            str: (lambda: self.deps.get('dateutil').parser.parse(date).strftime(self.DATE_FORMAT)),
            int: (lambda: self.deps.get('datetime').date.fromtimestamp(date).strftime(self.DATE_FORMAT)),
            float: (lambda: self.deps.get('datetime').date.fromtimestamp(date).strftime(self.DATE_FORMAT)),
            self.deps.get('datetime').date: (lambda: date.strftime(self.DATE_FORMAT))
        }.get(type(date))()

    def export(self):
        pass

    def run_tests(self):
        # Tests for date format
        assert s.normalize_date("04.02.1992") == "1992/04/02"
        assert s.normalize_date(1535516087) == "2018/08/28"
        assert s.normalize_date(1535516087.322354) == "2018/08/28"
        #  assert s.normalize_date(self.deps.get('datetime').date.today()) == "2018/08/28"


if (__name__ == "__main__"):

    from os import environ as env
    from sys import stdout
    s = SQLExporter('mssql', env['SQL_HOST'], env['SQL_PASSWORD'],
                    env['SQL_DB'], '~/.pysqlexport-output.csv', True, stdout)
