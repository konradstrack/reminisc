import logging
import mongoengine

from mongoengine import MultipleObjectsReturned, DoesNotExist

import reminisc.core.processing.commands as commands

from reminisc.core.storage import Storage
from reminisc.core.storage.mongo.domain import Contact, ContactIdentifier, Account, Message

logger = logging.getLogger(__name__)

class MongoDbStorage(Storage):
	"""Storage implementation using MongoDB"""

	def connect(self):
		"""Connects to a MongoDB database based on the settings in config.
		By default will not use any username nor password."""

		host = self.config.get('database', 'host')
		port = int(self.config.get('database', 'port'))
		database_name = self.config.get('database', 'database_name')

		username = self.config.get('database', 'username', fallback=None)
		password = self.config.get('database', 'password', fallback=None)

		mongoengine.connect(database_name, host=host, port=port, username=username, password=password)


	def store_message(self, command):
		# get account and contact references
		try:
			hints = [self.__get_account(handle, command) for handle in command.account_hints] if command.account_hints is not None else []
			print(command.account_hints)
			account = self.__get_account(command.account_id, command)
		except MultipleObjectsReturned:
			logger.error('Multiple accounts found for [{}, {}, {}]. Skipping message.'.format(command.account_id, 
				command.source, command.protocol))
			return

		try:
			contact = self.__get_contact(command)
		except MultipleObjectsReturned:
			logger.error('Multiple contacts found for [{}, {}, {}]. Skipping message.'.format(command.contact_id, 
				command.source, command.protocol))
			return

		datetime = command.datetime
		message = command.message
		direction = 'Received' if command.direction == commands.NewMessage.Direction.RECEIVED else 'Sent'

		Message(account=account, contact=contact, datetime=datetime, direction=direction, message=message).save()
		logger.debug("Message ({}): {}".format(command.direction, command.message))

	def __get_account(self, handle, command):
		try:
			account = Account.objects.get(handle=handle, source=command.source, 
				protocol=command.protocol)
		except DoesNotExist:
			account = Account(handle=handle, source=command.source, protocol=command.protocol)
			account.save()
	
		return account

	def __get_contact(self, command):
		try:
			contact = Contact.objects.get(identifiers__handle=command.contact_id,
				identifiers__protocol=command.protocol, identifiers__source=command.source)
		except DoesNotExist:
			identifier = ContactIdentifier(handle=command.contact_id,
				protocol=command.protocol, source=command.source)
			contact = Contact(name=command.contact_name, identifiers=[identifier])
			contact.save()

		return contact