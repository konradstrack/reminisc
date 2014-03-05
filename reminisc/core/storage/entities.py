from collections import namedtuple

Message = namedtuple('Message', ['text', 'datetime', 'direction', 'contact'])
Account = namedtuple('Account', ['id', 'name', 'handles', 'protocol', 'source'])