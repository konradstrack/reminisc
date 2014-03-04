class Message(object):
    def __init__(self, message, datetime, direction, contact):
        self.message = message
        self.datetime = datetime
        self.direction = direction
        self.contact = contact