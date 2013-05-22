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

	def execute(self):
		# we don't take any arguments for now
		parser = argparse.ArgumentParser()
		args = parser.parse_args()

		# TODO: add config location from command line
		configreader.create_config_file_if_not_exists(defaults.config_file_path)
		config = configreader.read_config_file(defaults.config_file_path)

		self.__start_processing()

		# filter enabled modules from config and start them
		enabled_modules = {k: v for (k, v) in config.items('modules') if v == 'True'}
		enabled_modules_names = map(lambda item: item[0], enabled_modules.items())

		self.__start_modules(enabled_modules_names)

	def __start_processing(self):
		def process_tasks():
			logger.info("Starting processor")
			processor = tasks.TaskProcessor(queues.tasks_queue)
			processor.start()

		thread = threading.Thread(target=process_tasks)
		thread.deamon = True
		thread.start()

	def __start_modules(self, modules):
		for module_path in modules:
			logger.info("Starting module: {}".format(module_path))
			module = importlib.import_module(module_path)

			thread = threading.Thread(target=module.start_module)
			thread.daemon = True
			thread.start()