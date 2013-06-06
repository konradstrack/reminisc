from mongoengine import StringField, ReferenceField, ListField, DateTimeField, BooleanField, EmbeddedDocumentField
from mongoengine import Document, EmbeddedDocument

class ContactIdentifier(EmbeddedDocument):
	handle = StringField()
	protocol = StringField()
	source = StringField()

class Contact(Document):
	name = StringField()
	identifiers = ListField(EmbeddedDocumentField(ContactIdentifier))

class Account(Document):
	name = StringField()
	handle = StringField()
	protocol = StringField()
	source = StringField()
	
class Message(Document):
	contact = ReferenceField(Contact)
	account = ReferenceField(Account)
	
	datetime = DateTimeField()
	incoming = BooleanField()
	message = StringField()
