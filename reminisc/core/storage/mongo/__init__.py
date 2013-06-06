import logging
import mongoengine

import reminisc.core.processing.commands as commands

from reminisc.core.storage import Storage
from reminisc.core.storage.mongo.domain import Contact, Account, Message

logger = logging.getLogger(__name__)

class MongoDbStorage(Storage):
	"""Storage implementation using MongoDB"""

	def connect(self):
		"""Connects to a MongoDB database based on the settings in config.
		By default will use no username nor password."""

		host = self.config.get('database', 'host')
		port = int(self.config.get('database', 'port'))
		database_name = self.config.get('database', 'database_name')

		username = self.config.get('database', 'username', fallback=None)
		password = self.config.get('database', 'password', fallback=None)

		mongoengine.connect(database_name, host=host, port=port, username=username, password=password)


	def store_message(self, command):
		datetime = command.datetime
		message = command.message
		incoming = True if command.direction == commands.NewMessage.Direction.RECEIVED else False

		Message(datetime=datetime, incoming=incoming, message=message).save()
		logger.debug("Message ({}): {}".format(command.direction, command.message))