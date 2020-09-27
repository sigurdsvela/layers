import layers.clid.commands
import layers.clid.argtype

commands = layers.clid.commands
argtype = layers.clid.argtype



class Runner:

	def run(self, command, **kwargs):
		import sys
		import os

		nullfh = None
		if self._qstdout or self._qstderr:
			nullfh = open(os.devnull, 'w')
			self._stdout = nullfh if self._qstdout else self._stdout
			self._stderr = nullfh if self._qstderr else self._stderr

		with self._stdout as sys.stdout, self._stdin as sys.stdin, self._stderr as sys.stderr:
			command.run(**kwargs)

		if nullfh:
			nullfh.close()

	def __init__(self):
		import sys
		self._qstdout = False
		self._qstderr = False
		self._stdout = sys.stdout
		self._stdin = sys.stdin
		self._stderr = sys.stdin

	def quiet(self, stdout=True, stderr=False):
		self._qstdout = stdout
		self._qstderr = stderr

	def stdio(self, stdout = None, stdin = None, stderr = None):
		if stdout is not None:
			self._stdout = stdout
		if stdin is not None:
			self._stdin = stdin
		if stderr is not None:
			self._stderr = stderr
