import logging

logger = logging.getLogger(__name__)

class Task(object):
	"""Single task to perform, e.g. containing a message to store received from the client."""

	def __init__(self, command):
		self.command = command


class TaskProcessor(object):
	"""Processes tasks available in the queue."""

	def __init__(self, queue):
		self.queue = queue

	def _process_next(self):
		task = self.queue.get()

		# TODO: this is temporary, do something useful here
		logger.info("Processing - {}".format(task.command))

	def start(self):
		while True:
			self._process_next()