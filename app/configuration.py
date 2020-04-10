import os
import json

class Configuration():

	_CONFIGURATION_FILE = '/configuration.json'

	def load(self):
		with open(os.getcwd() + self._CONFIGURATION_FILE, "r") as handle:
			config = json.load(handle)
			return config

