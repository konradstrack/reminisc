import reminisc.config.reader as reader

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