from datetime import datetime
import logging
from filepaths import logs_filepath

def configure_logger():
	current_datetime = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
	log_filename = "log-{}.txt".format(current_datetime)
	log_file = logs_filepath + log_filename
	log_stream = 'sys.stdout'
	log_level = logging.DEBUG
	log_format = "%(asctime)s %(levelname)s: %(message)s"
	log_date_format = "%m/%d/%Y %H:%M:%S"
	logging.basicConfig(filename=log_file, level=log_level, format=log_format, datefmt=log_date_format)
