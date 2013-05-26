import random
import time
import reminisc.core.processing.tasks as tasks

from reminisc.modules.abstract_module import AbstractModule

def start_module(global_config, module_config):
	module = ExampleClientModule(global_config, module_config)
	module.start()

class ExampleClientModule(AbstractModule):

	def __init__(self, global_config, module_config, command_queue):
		super().__init__(global_config, module_config, command_queue)

		self.commands = ["first", "second", "third"]

	def should_be_started(self):
		return True

	def start(self):
		while True:
			interval = float(self.module_config.get("defaults", "time_interval", fallback = 1))
			time.sleep(interval)
			self.__generate_task()

	def __generate_task(self):
		command = random.choice(self.commands)
		task = tasks.Task(command)

		self.command_queue.put(task)