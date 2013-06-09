from datetime import date

from reminisc.core.processing.commands import NewMessage

class TestNewMessage(object):

	def test_if_all_fields_are_set(self):
		source = 'source'
		account_id = 'account-id'
		contact_id = 'contact-id'
		today = date.today()
		message_text = 'my message'
		direction = NewMessage.Direction.RECEIVED

		contact_name = 'Some Contact'

		kwargs1 = {'contact_name': contact_name}

		message = NewMessage(source, account_id, contact_id, today, message_text, direction, **kwargs1)

		assert source == message.source
		assert account_id == message.account_id
		assert contact_id == message.contact_id
		assert today == message.datetime
		assert message_text == message.message
		assert NewMessage.Direction.RECEIVED == message.direction

		assert contact_name == message.contact_name
		assert None == message.protocol
		assert None == message.account_hints