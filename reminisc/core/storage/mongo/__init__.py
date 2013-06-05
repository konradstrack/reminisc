import logging

from reminisc.core.storage import Storage

logger = logging.getLogger(__name__)

class MongoDbStorage(Storage):
	"""Storage implementation using MongoDB"""

	def connect(self):
		pass

	def store_message(self, command):
		logger.debug("Message ({}): {}".format(command.direction, command.message))