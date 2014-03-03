import logging

from reminisc.modules.abstract_module import AbstractModule
from reminisc.modules.gajim_import.importer import IterativeImporter

logger = logging.getLogger(__name__)


class GajimImportModule(AbstractModule):
    def should_be_started(self):
        return True

    def start(self):
        importer = IterativeImporter(self.module_config, self.dbconfig, self.command_queue)
        importer.start()

    @staticmethod
    def default_config():
        return open('reminisc/modules/gajim_import/config/default.ini', 'r').read()