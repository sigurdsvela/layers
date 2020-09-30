from subprocess import Popen
from layers.lib import Layer, LayerFile, LayerSet, UserConfig
from unittest import TestCase

class LayersLibTestCase(TestCase):
	def setUp(self):
		self.config = UserConfig.forCurrentUser()
		Popen(['rm', '-rf', self.config.path]).wait()
		self.config = UserConfig.forCurrentUser()

	def tearDown(self):
		Popen(['rm', '-rf', self.config.path]).wait()

	def assertEqual(self, first, second, msg=None):
		if isinstance(first, Layer) and isinstance(second, Layer):
			return super().assertEqual(first, second, f"{first.root} != {second.root}")
		if isinstance(first, LayerSet) and isinstance(second, LayerSet):
			return super().assertEqual(first, second, f"{first.name} != {second.name}")
		if isinstance(first, UserConfig) and isinstance(second, UserConfig):
			return super().assertEqual(first, second, f"{first.home} != {second.home}")
		if isinstance(first, LayerFile) and isinstance(second, LayerFile):
			return super().assertEqual(first, second, f"{first.absolute} != {second.absolute}")
		return super().assertEqual(first, second, msg=None)
	

	def assertFileExist(self, file: LayerFile, msg = None):
		resolvedPath = file.absolute.resolve(strict=False)
		if msg is None:
			if file.isSymlink():
				fs = f"{str(file.absolute)} -> {str(resolvedPath)}"
			else:
				fs = f"{str(file.absolute)}"
			msg = f"Failed to assert that file {fs} exists"

		if not resolvedPath.exists():
			raise self.failureException(msg)
	
	def assertUnorderedListsEqual(self, first, second, msg = None):
		for e in first:
			try:
				idx = second.index(e)
				del second[idx]
			except:
				raise self.failureException(msg if msg is not None else f"Elements {e} not found in {second}")

		for e in second:
			try:
				idx = first.index(e)
				del first[idx]
			except:
				raise self.failureException(msg if msg is not None else f"Elements {e} not found in {first}")
