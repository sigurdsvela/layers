import layers.clid.commands
import layers.clid.argtype
from io import StringIO
from argparse import ArgumentParser
from pathlib import Path
import logging
import sys

commands = layers.clid.commands
argtype = layers.clid.argtype

logLevel = logging.WARNING

root = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
root.setLevel(logLevel)
handler.setLevel(logLevel)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

class Runner:
	@classmethod
	def globalDefaults(cls):
		import os
		return { 'target_layer': Path(os.getcwd()) }

	def run(self, command, **kwargs):
		logger = logging.getLogger(".".join([__name__, "Runner"]))
		
		logger.debug(f"Running command {command} with args: ")
		logger.debug(kwargs)
		import sys

		_stdout = sys.stdout
		_stdout = sys.stdout

		if self._qstdout:
			sys.stdout = StringIO()

		if self._qstderr:
			sys.stdout = StringIO()

		if self._defaults:
			kwargs = dict(dict(__class__.globalDefaults(), **command.defaults), **kwargs)

		try:
			return command.run(**kwargs)
		except Exception as e:
			raise e
		finally:
			sys.stdout = _stdout
			sys.stdout = _stdout


	def __init__(self):
		self._qstdout = False
		self._qstderr = False
		self._stdout = None
		self._stderr = None
		self._defaults = False

	def quiet(self, stdout=True, stderr=False):
		self._qstdout = stdout
		self._qstderr = stderr
		return self
		
	def applyDefaults(self):
		self._defaults = True
		return self
