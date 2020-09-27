from pathlib import Path
from typing import Union

class FSStruct:
	def __init__(self, rootPath: Path, rootDir):
		pass
	

class FSPath:
	def __init__(self, path: str):
		self._parts = path.split("/")

	def __str__(self):
		return "/".join(self._parts)

	@property
	def parts(self):
		return self._parts

class FSUnit:
	pass

class FSDir(FSUnit):
	def __init__(self):
		self.units: [FSUnit] = []

	def __setitem__(self, *key: [str], value: FSUnit):
		pass


class FSFile(FSUnit):
	def __init__(self, content: str):
		pass