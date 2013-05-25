import unittest
import reminisc.config.reader as reader

class ConfigDictTest(unittest.TestCase):

	def setUp(self):
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
		self.assertTrue(self.configdict.contains('Section A', 'Option 1'))
		self.assertTrue(self.configdict.contains('Section B', 'Option 3'))

	def test_should_not_contain_options(self):
		self.assertFalse(self.configdict.contains('Section A', 'Option 3'))
		self.assertFalse(self.configdict.contains('Not a section', 'Option 1'))
		self.assertFalse(self.configdict.contains('Section A', 'Not an option'))

	def test_should_get_value(self):
		self.assertEqual('Fry', self.configdict.get('Section B', 'Option 3'))
		self.assertEqual(3000, self.configdict.get('Section A', 'Option 1'))

	def test_should_get_default_value(self):
		self.assertEquals('Leela', self.configdict.get('Not a section', 'Not an option', fallback = 'Leela'))

	def test_should_raise_exception(self):
		self.assertRaises(KeyError, self.configdict.get, 'Not a section', 'Not an option')