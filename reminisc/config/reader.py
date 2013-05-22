import os
import logging
import shutil
import configparser
import reminisc.config.defaults as defaults

logger = logging.getLogger(__name__)

def create_config_file_if_not_exists(path):
	# no default config file
	if not os.path.isfile(path):

		directory = os.path.dirname(path)

		# no default directory
		if not os.path.isdir(directory):
			os.mkdir(directory)

		shutil.copyfile('reminisc/config/default_config.ini', path)

def read_config_file(path):
	config = configparser.ConfigParser()
	config.read(path)

	return config