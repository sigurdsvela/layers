from unittest import TestCase
from layers.lib import LayerSet, UserConfig, Layer
from pathlib import Path
import subprocess
import shutil

class TestLayer(TestCase):
	def setUp(self):
		self.config = UserConfig.forCurrentUser()
		subprocess.Popen(["rm", "-rf", (self.config.path)]).wait()
		self.config = UserConfig.forCurrentUser()

		self.rootSet = self.config.addLayerSet(name='root')

		self.layer = self.config.addLayer(
			layer=Layer(layerSet=self.rootSet, root=Path('~/test-layer1').expanduser()),
			toSet=self.rootSet
		)

		self.layer.root.mkdir()

	def tearDown(self):
		subprocess.Popen(["rm", "-rf", (self.config.path)]).wait()
		subprocess.Popen(["rm", "-rf", (self.layer.root)]).wait()
		self.assertFalse(self.config.path.exists())

	def test_simpleShallowPurge(self):
		(self.layer.root/"testfile").symlink_to(Path("Broken"))
		self.assertTrue((self.layer.root/"testfile").is_symlink())
		self.layer.purge()
		self.assertFalse((self.layer.root/"testfile").exists())

	def test_inDirectoryPurge(self):
		testDir = (self.layer.root/"testDir")
		testDir.mkdir()
		testFile = (testDir/"testfile")
		testFile.symlink_to(Path("Broken"))
		self.assertTrue(testFile.is_symlink())
		self.layer.purge()
		self.assertFalse(testFile.exists())

	def test_getFiles(self):
		testDir = (self.layer.root/"testDir")
		testDir.mkdir()
		testFiles = [
			(testDir/"testfile1"),
			(testDir/"testfile2"),
			(testDir/"testfile3"),
			(self.layer.root/"testfile1"),
			(self.layer.root/"testfile2"),
			(self.layer.root/"testfile3"),
		]

		for testFile in testFiles:
			testFile.touch()

		for f in self.layer.files:
			testFiles.index(f.absolute)
		
		files = [f.absolute for f in self.layer.files]
		for f in testFiles:
			files.index(f)

	def test_findPurelyDerivativeDir(self):
		# TODO
		pass


	