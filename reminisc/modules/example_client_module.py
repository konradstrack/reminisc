import random
import time
import reminisc.core.processing.tasks as tasks
import reminisc.core.processing.queues as queues

def start_module():
	module = ExampleClientModule()
	module.start()

class ExampleClientModule(object):

	def __init__(self):
		self.commands = ["first", "second", "third"]
		self.queue = queues.tasks_queue

	def start(self):
		while True:
			time.sleep(1)
			self.__generate_task()

	def __generate_task(self):
		command = random.choice(self.commands)
		task = tasks.Task(command)

		self.queue.put(task)