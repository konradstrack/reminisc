import pytest
import reminisc.config.reader as reader

class TestConfigDict(object):

	def setup_method(self, method):
		self.testdict = {
			'Section A' : {
				'Option 1' : 3000,
				'Option 2' : 'Zoidberg'
			},
			'Section B' : {
				'Option 3' : 'Fry'
			}
		}

		self.configdict = reader.ConfigDict(self.testdict)

	def test_should_contain_options(self):
		assert self.configdict.contains('Section A', 'Option 1')
		assert self.configdict.contains('Section B', 'Option 3')

	def test_should_not_contain_options(self):
		assert not self.configdict.contains('Section A', 'Option 3')
		assert not self.configdict.contains('Not a section', 'Option 1')
		assert not self.configdict.contains('Section A', 'Not an option')

	def test_should_get_value(self):
		assert 'Fry' == self.configdict.get('Section B', 'Option 3')
		assert 3000 == self.configdict.get('Section A', 'Option 1')

	def test_should_get_default_value(self):
		assert 'Leela' == self.configdict.get('Not a section', 'Not an option', fallback = 'Leela')

	def test_should_raise_exception(self):
		with pytest.raises(KeyError):
			self.configdict.get('Not a section', 'Not an option')

class TestReminiscConfigParser(object):

	def setup_method(self, method):	
		configstring = """
			[Section A]
			option 1 = 3000

			[Section B]
			option 3 = Fry
		"""

		self.parser = reader.ReminiscConfigParser()
		self.parser.read_string(configstring)

	def test_should_contain_valuse_from_config(self):
		configdict = self.parser.as_config_dict()
		assert 'Fry' == configdict.get('Section B', 'option 3')
		assert 3000 == int(configdict.get('Section A', 'option 1'))