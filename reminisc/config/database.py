import sqlite3

class DbConfig(object):

	def __init__(self, db_path, prefix=None):
		self.__db_path = db_path
		if prefix is None:
			self.__prefix = None
		else:
			self.__prefix = prefix + '.'

		self.__conn = None

	def connect(self):
		"""Connects to the config database."""

		self.__conn = sqlite3.connect(self.__db_path)
		self.__conn.row_factory = sqlite3.Row

	def close(self):
		"""Closes connection to the config database."""

		if self.__conn is not None:
			self.__conn.close()

		self.__conn = None

	def get(self, key):
		"""Returns value for the given key. Raises KeyError if it doesn't exist."""

		pkey = self.__prefixed(key)
		result = self.__conn.execute('select * from settings where key=?', (pkey,)).fetchone()

		if result is None:
			raise KeyError('There\'s no such key {} in the settings table'.format(pkey))

		return result['value']

	def save(self, key, value):
		"""Saves value under the given key."""

		pkey = self.__prefixed(key)
		self.__conn.execute('insert into settings(key,value) values (?,?)', (pkey, value))
		self.__conn.commit()

	def __prefixed(self, key):
		return self.__prefix + key
