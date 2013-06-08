from mongoengine import StringField, ReferenceField, ListField, DateTimeField, BooleanField, EmbeddedDocumentField
from mongoengine import Document, EmbeddedDocument

class ContactIdentifier(EmbeddedDocument):
	handle = StringField(required=True)
	protocol = StringField()
	source = StringField(required=True)

class Contact(Document):
	name = StringField()
	identifiers = ListField(EmbeddedDocumentField(ContactIdentifier))

class Account(Document):
	name = StringField()
	handle = StringField()
	protocol = StringField()
	source = StringField(required=True)
	
class Message(Document):
	contact = ReferenceField(Contact)
	account = ReferenceField(Account)
	
	account_hints = ListField(ReferenceField(Account))

	datetime = DateTimeField()
	direction = StringField(choices=('Received', 'Sent'), required=True)
	message = StringField()
