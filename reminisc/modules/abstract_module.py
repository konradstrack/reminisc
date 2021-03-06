import abc


class AbstractModule(metaclass=abc.ABCMeta):
    """This abstract class should be inherited by all Reminisc modules.
    Only modules extending this class will be instantiated and executed."""

    def __init__(self, global_config, module_config, command_queue, dbconfig):
        """Global config for the application, and specific config for the module
        are passed during instantiation."""

        self.global_config = global_config
        self.module_config = module_config
        self.command_queue = command_queue
        self.dbconfig = dbconfig

    @abc.abstractmethod
    def should_be_started(self):
        """Return True if module should be started, False otherwise.
        This may be used to decide if it should be possible to use the module."""

        return

    @abc.abstractmethod
    def start(self):
        """This method starts the module.
        It will be executed if should_be_started() method returns True."""

        return

    @staticmethod
    @abc.abstractmethod
    def default_config():
        """Returns content of the default config file for this module"""

        return