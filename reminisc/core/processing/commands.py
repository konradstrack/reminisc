import logging

logger = logging.getLogger(__name__)

class Command(object):
	"""Single command to perform, e.g. containing a message to store received from the client."""

	def __init__(self, command):
		self.command = command


class NewMessage(object):
	"""Represents command to create (save) a new messages"""

	def __init__(self, content):
		self.content = content

class NewContact(object):
	"""Represents command to create (save) a new contact"""

	def __init__(self, name):
		self.name = name
