import argparse
import threading
import importlib
import logging

import reminisc.core.processing.queues as queues
import reminisc.core.processing.processor as processor
import reminisc.modules.abstract_module as am
import reminisc.config.reader as config_reader
import reminisc.config.generator as config_generator
import reminisc.config.defaults as defaults
import reminisc.modules.utils as module_utils

from reminisc.config.database import DbConfig

logger = logging.getLogger(__name__)

class Application(object):
	"""Main class of the application containing logic to parse configuration and start all components."""

	def execute(self):
		"""Starts the application."""

		# we don't take any arguments for now
		parser = argparse.ArgumentParser()
		parser.add_argument('--config-directory', help='config directory location')
		parser.add_argument('--create-config', action='store_true', help='generate default configuration files')
		args = parser.parse_args()

		# determine config directory location
		self.__config_dir = args.config_directory if args.config_directory else defaults.config_folder_path

		# generate config if should be generated end stop execution
		if args.create_config:
			print("Generating config directory: {}".format(self.__config_dir))
			config_generator.create_config_directory(self.__config_dir)
			return

		self.__config = config_reader.read_config_file(defaults.get_global_config_path(self.__config_dir))

		self.__start_processing()

		# filter enabled modules from config and start them
		enabled_modules = {k: v for (k, v) in self.__config.items('modules') if v == 'True'}
		enabled_modules_names = map(lambda item: item[0], enabled_modules.items())

		self.__start_modules(enabled_modules_names)

	def __start_processing(self):
		"""Starts threads responsible for processing incoming data."""

		def process_commands():
			logger.info("Starting processor")
			command_processor = processor.CommandProcessor(queues.command_queue)
			command_processor.start()

		thread = threading.Thread(target=process_commands)
		thread.deamon = True
		thread.start()

	def __start_modules(self, modules):
		"""Responsible for starting all enabled modules in separate threads."""

		global_config_dict = self.__config.as_config_dict()
		queue = queues.command_queue

		for module_name in modules:
			logger.debug("Inspecting module: {}".format(module_name))

			# parse module config and convert it to a dict
			config = config_reader.read_config_file(defaults.get_module_config_path(self.__config_dir, module_name))
			config_dict = config.as_config_dict()

			# find all classes in the module extending AbstractModule
			reminisc_module_impls = module_utils.find_reminisc_module_implementations(module_name)

			# only one class extending AbstractModule is going to be started per reminisc module
			if len(reminisc_module_impls) > 1:
				logger.error("Module {} has more than 1 module class. Module will not be started.".format(module_name))
			else:
				for impl in reminisc_module_impls:
					# instantiate the module class
					dbpath = defaults.get_config_database_path(self.__config_dir)
					dbconfig = DbConfig(dbpath, prefix=module_name)
					mod_instance = impl(global_config_dict, config_dict, queue, dbconfig)

					# start thread for the module if can be started
					if mod_instance.should_be_started():
						logger.info("Starting {}".format(impl.__name__))

						thread = threading.Thread(target=mod_instance.start)
						thread.daemon = True
						thread.start()
					else:
						logger.warn("Module class {} is disabled".format(impl.__name__))