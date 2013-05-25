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
	config = ReminiscConfigParser()
	config.read(path)

	return config

class ReminiscConfigParser(configparser.ConfigParser):

	def as_config_dict(self):
		sections = dict(self._sections)
		for key in sections:
			sections[key] = dict(self._defaults, **sections[key])
			sections[key].pop('__name__', None)

		return ConfigDict(sections)

class ConfigDict(object):

	 def __init__(self, dictionary):
	 	self.__dict = dictionary

	 def contains(self, section, option):
	 	return section in self.__dict and option in self.__dict[section]

	 def get(self, section, option, fallback=None):
	 	if self.contains(section, option):
	 		return self.__dict[section][option]
	 	elif fallback is not None:
	 		return fallback
	 	else:
	 		raise KeyError("There's no such option in the config")


