import argparse
import threading
import importlib
import logging
import reminisc.core.processing.queues as queues
import reminisc.core.processing.tasks as tasks
import reminisc.modules as modules

logger = logging.getLogger(__name__)

class Application(object):

	def execute(self):
		# we don't take any arguments for now
		parser = argparse.ArgumentParser()
		args = parser.parse_args()

		self.__start_processing()
		self.__start_modules()

	def __start_processing(self):
		def process_tasks():
			logger.info("Starting processor")
			processor = tasks.TaskProcessor(queues.tasks_queue)
			processor.start()

		thread = threading.Thread(target=process_tasks)
		thread.deamon = True
		thread.start()

	def __start_modules(self):
		for module_path in modules.registered_modules:
			logger.info("Starting module: {}".format(module_path))
			module = importlib.import_module(module_path)

			thread = threading.Thread(target=module.start_module)
			thread.daemon = True
			thread.start()