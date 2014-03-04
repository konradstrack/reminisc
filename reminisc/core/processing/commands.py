import logging
from reminisc.core.utils import Enum

logger = logging.getLogger(__name__)


class Command(object):
    """Single command to perform, e.g. containing a message to store received from the client."""

    def __init__(self, command):
        self.command = command


class NewMessage(object):
    """Represents command to create (save) a new messages"""

    # an enum representing direction
    Direction = Enum(['RECEIVED', 'SENT'])

    def __init__(self, source, account_ids, contact_id, datetime, message, direction, **kwargs):
        """Constructs the new-message command.

        :param source: source of the message, e.g. 'Gajim'
        :param account_ids: list of unique identifiers of user's account (e.g. jid)
        :param contact_id: unique identifier of the contact (e.g. jid)
        :param datetime: message creation time
        :param message: content of the message
        :param direction: Direction.RECEIVED or Direction.SENT (received or sent by the account)
        """

        self.source = source
        self.account_ids = account_ids
        self.contact_id = contact_id
        self.datetime = datetime
        self.message = message
        self.direction = direction

        self.contact_name = kwargs.get('contact_name', None)
        self.protocol = kwargs.get('protocol', None)


class NewContact(object):
    """Represents command to create (save) a new contact"""

    def __init__(self, name):
        self.name = name
