import os
import logging
import shutil
import configparser
import reminisc.config.defaults as defaults

logger = logging.getLogger(__name__)

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

# to allow passing None as a fallback in ConfigDict.get()
sentinel = object()

class ConfigDict(object):

	 def __init__(self, dictionary):
	 	self.__dict = dictionary

	 def contains(self, section, option):
	 	return section in self.__dict and option in self.__dict[section]

	 def get(self, section, option, fallback=sentinel):
	 	if self.contains(section, option):
	 		return self.__dict[section][option]
	 	elif fallback is not sentinel:
	 		return fallback
	 	else:
	 		raise KeyError("There's no such option in the config")


