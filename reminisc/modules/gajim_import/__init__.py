import logging
import reminisc.core.processing.commands as commands
import reminisc.core.processing.queues as queues

from reminisc.modules.abstract_module import AbstractModule

logger = logging.getLogger(__name__)

class GajimImportModule(AbstractModule):

	# def __init__(self, global_config, module_config, command_queue):
	# 	super().__init__(global_config, module_config, command_queue)

	def should_be_started(self):
		return True

	def start(self):
		pass

	@staticmethod
	def default_config():
		return open('reminisc/modules/gajim_import/config/default.ini', 'r').read()