import argparse
import threading
import importlib
import logging
import reminisc.core.processing.queues as queues
import reminisc.core.processing.tasks as tasks
import reminisc.modules as modules
import reminisc.config.reader as configreader
import reminisc.config.defaults as defaults

logger = logging.getLogger(__name__)

class Application(object):
	"""Main class of the application containing logic to parse configuration and start all components."""

	def execute(self):
		"""Starts the application."""

		# we don't take any arguments for now
		parser = argparse.ArgumentParser()
		args = parser.parse_args()

		# TODO: add config location from command line
		configreader.create_config_file_if_not_exists(defaults.config_file_path)
		self.__config = configreader.read_config_file(defaults.config_file_path)

		self.__start_processing()

		# filter enabled modules from config and start them
		enabled_modules = {k: v for (k, v) in self.__config.items('modules') if v == 'True'}
		enabled_modules_names = map(lambda item: item[0], enabled_modules.items())

		self.__start_modules(enabled_modules_names)

	def __start_processing(self):
		"""Starts threads responsible for processing incoming data."""

		def process_tasks():
			logger.info("Starting processor")
			processor = tasks.TaskProcessor(queues.tasks_queue)
			processor.start()

		thread = threading.Thread(target=process_tasks)
		thread.deamon = True
		thread.start()

	def __start_modules(self, modules):
		"""Responsible for starting all enabled modules in separate threads."""

		global_config_dict = self.__config.as_config_dict()

		for module_path in modules:
			logger.info("Starting module: {}".format(module_path))

			# parse module config and convert it to a dict
			module_config = configreader.read_config_file(defaults.get_module_config_file(module_path))
			module_config_dict = module_config.as_config_dict()

			# import the module
			module = importlib.import_module(module_path)

			# start thread for the module
			thread = threading.Thread(target=module.start_module, args=(global_config_dict, module_config_dict))
			thread.daemon = True
			thread.start()