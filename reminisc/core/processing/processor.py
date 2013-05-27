import logging
import reminisc.core.processing.commands as commands
import reminisc.core.dispatcher as dispatcher

logger = logging.getLogger(__name__)

dispatch = dispatcher.TypeDispatcher()

class CommandProcessor(object):
	"""Processes tasks available in the queue."""

	def __init__(self, queue):
		self.queue = queue

	def _process_next(self):
		task = self.queue.get()
		self.process(task)

	def start(self):
		while True:
			self._process_next()

	@dispatch.when(commands.NewMessage)
	def process(self, command):
		logger.debug("New message: {}".format(command))

	@dispatch.when(commands.NewContact)
	def process(self, command):
		logger.debug("New contact: {}".format(command))

	@dispatch.default
	def process(self, command):
		logger.debug("Default processor: {}".format(command))

	# TODO: rewrite dispatcher, so that this method doesn't have to be the last one
	@dispatch.on
	def process(self, command):
		pass