#!/usr/bin/python

class SQLExporter(object):

	def __init__(self, dbdriver = 'mysql', host = 'localhost', password = None, db, output_filename = 'output.csv'):
		self.host = host
		self.password = password
		self.db = db
		self.output_filename = output_filename

		# Define the delimiters we will use
		DELIMITER_COMMA = "," # Spec calls for ascii 20


	def export(self):


if (__name__ == "__main__"):
	s = SQLExporter()