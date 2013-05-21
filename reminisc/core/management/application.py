import argparse

class Application(object):

	def execute(self):
		parser = argparse.ArgumentParser()
		args = parser.parse_args()
