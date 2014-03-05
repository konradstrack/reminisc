import abc


class Storage(metaclass=abc.ABCMeta):
    def __init__(self, config):
        """Constructs storage, but does not connect to anything.

        :param config: configuration dictionary for the storage implementation
        """

        self.config = config

    @abc.abstractmethod
    def connect(self):
        """Connects to the storage."""
        pass

    @abc.abstractmethod
    def store_message(self, command):
        """Stores message based on the given command"""
        pass

    @abc.abstractmethod
    def get_messages(self, account_handles, **kwargs):
        """Retrieves messages and returns them in a database agnostic form"""
        pass

    @abc.abstractmethod
    def get_accounts(self, **kwargs):
        """Retrieves accounts and returns them in a database agnostic form"""
        pass