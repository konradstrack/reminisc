import logging
import mongoengine

from mongoengine import MultipleObjectsReturned, DoesNotExist

import reminisc.core.processing.commands as commands
from reminisc.core.storage import Storage

from reminisc.core.storage.entities import Message as DTOMessage
from reminisc.core.storage.mongo.domain import Contact, ContactIdentifier, Account, Message

logger = logging.getLogger('root')


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

        mongoengine.connect(database_name, host=host, port=port, username=username,
                            password=password)


    def store_message(self, command):
        # get account and contact references
        try:
            account = self.__get_account(command.account_ids, command)
        except MultipleObjectsReturned:
            logger.error('Multiple accounts found for [{}, {}, {}]. Skipping message.'.format(
                command.account_ids, command.source, command.protocol))
            return

        try:
            contact = self.__get_contact(command)
        except MultipleObjectsReturned:
            logger.error('Multiple contacts found for [{}, {}, {}]. Skipping message.'.format(
                command.contact_id, command.source, command.protocol))
            return

        datetime = command.datetime
        message = command.message

        if command.direction == commands.NewMessage.Direction.RECEIVED:
            direction = 'Received'
        else:
            direction = 'Sent'

        Message(account=account, contact=contact, datetime=datetime,
                direction=direction, message=message).save()

        logger.debug("Message ({}): {}".format(command.direction, command.message))

    def get_messages(self, account_handle, **kwargs):
        try:
            accounts = Account.objects(handles__in=[account_handle])
        except DoesNotExist:
            return []

        messages = Message.objects(account__in=accounts).all()[:20]
        return [DTOMessage(msg.message, msg.datetime, msg.direction, msg.contact.name) for msg in messages]

    def __get_account(self, handles, command):
        try:
            account = Account.objects.get(handles=handles, source=command.source,
                                          protocol=command.protocol)
        except DoesNotExist:
            account = Account(handles=handles, source=command.source, protocol=command.protocol)
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