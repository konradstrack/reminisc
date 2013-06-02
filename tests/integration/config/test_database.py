import pytest
import reminisc.config.database as db
import reminisc.config.generator as generator

class TestDbConfig(object):

	def get_dbconfig(self, tmpdir):
		dbfile = tmpdir.join('config.db')
		generator.create_config_database(str(dbfile))
		dbconfig = db.DbConfig(str(dbfile), prefix='my.prefix')
		dbconfig.connect()

		return dbconfig

	def test_if_raises_error_for_wrong_keys(self, tmpdir):
		dbconfig = self.get_dbconfig(tmpdir)

		with pytest.raises(KeyError):
			dbconfig.get('wrong-key')

	def test_if_saves_and_gets_same_value(self, tmpdir):
		dbconfig = self.get_dbconfig(tmpdir)
		key = 'correct-key'
		value = 'correct-value'

		dbconfig.save(key, value)
		assert value == dbconfig.get(key)
