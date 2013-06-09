import pytest
import queue

from unittest.mock import Mock, MagicMock

from reminisc.core.processing.processor import CommandProcessor
from reminisc.core.processing.commands import NewMessage

class TestProcessor(object):

	def setup_method(self, method):
		self.storage = Mock()
		self.storage.connect = MagicMock()
		self.storage.store_message = MagicMock()

	def test_if_takes_tasks_to_process(self):
		test_queue = queue.Queue()

		processor = CommandProcessor(test_queue, self.storage)
		processor.process = Mock()

		command = Mock(spec=NewMessage)
		test_queue.put(command)

		processor._process_next()
		processor.process.assert_called_with(command)

	def test_if_tries_to_store_new_message(self):
		command = Mock(spec=NewMessage)

		processor = CommandProcessor(queue.Queue(), self.storage)
		processor.process(command)

		self.storage.store_message.assert_called_with(command)
