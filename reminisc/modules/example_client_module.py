import random
import time
import reminisc.core.processing.tasks as tasks
import reminisc.core.processing.queues as queues

def start_module(global_config, module_config):
	module = ExampleClientModule(global_config, module_config)
	module.start()

class ExampleClientModule(object):

	def __init__(self, global_config, module_config):
		self.__global_config = global_config
		self.__module_config = module_config

		self.commands = ["first", "second", "third"]
		self.queue = queues.tasks_queue

	def start(self):
		while True:
			interval = float(self.__module_config.get("defaults", "time_interval", fallback = 1))
			time.sleep(interval)
			self.__generate_task()

	def __generate_task(self):
		command = random.choice(self.commands)
		task = tasks.Task(command)

		self.queue.put(task)