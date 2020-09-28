import subprocess
import os
from testlib.BasicLayerCase import BasicLayerCase
from layers.cli import Runner
from layers.clid import commands
from pprint import PrettyPrinter

class TestMove(BasicLayerCase):
	def setUp(self):
		super().setUp()
		syncErrors = super().sync()
		if syncErrors:
			raise syncErrors[0]
	
	def test_moveUpDown(self):
		import contextlib
		os.chdir(self.layers[0].path)
		runner = Runner().applyDefaults()

		testFile = self.filesIn(level=2)[0]

		runner.run(command=commands.Move, level="up", path=testFile.path)
		self.assertTrue(testFile.path.is_symlink())	
		self.assertFalse(testFile.inLayer(layer=self.layers[1]).path.is_symlink())	

		testFile = self.filesIn(level=0)[0]
		runner.run(command=commands.Move, level="down", path=testFile.path)
		self.assertTrue(testFile.path.is_symlink())	
		self.assertFalse(testFile.inLayer(layer=self.layers[1]).path.is_symlink())

		self.assertVerify()
		

	def test_moveTopBottom(self):
		runner = Runner().applyDefaults()
		os.chdir(self.layers[0].path)
		
		testFile = self.filesIn(level=-1)[0]
		runner.run(command=commands.Move, level='top', path=testFile.path)
		self.assertTrue(testFile.path.is_symlink())	
		self.assertFalse(testFile.inLayer(layer=self.layers[0]).path.is_symlink())	


		testFile = self.filesIn(level=0)[0]
		runner.run(command=commands.Move, level='bottom', path=testFile.path)
		self.assertTrue(testFile.path.is_symlink())	
		self.assertFalse(testFile.inLayer(layer=self.layers[-1]).path.is_symlink())	

		self.assertVerify()

	def test_renameFile(self):
		os.chdir(self.layers[0].path)
		runner = Runner().applyDefaults()

		testFile = self.files[0]
		newName = '46031CAD-C9C0-4E79-9BCA-AF9C876C3EC0'

		try:
			runner.run(command=commands.Move, level='bottom', path=testFile.localPath, new_path=testFile.withName(newName).localPath)
		except Exception as e:
			self.printFsStruct()
			raise e
		
		self.assertFalse(testFile.path.exists())
		self.assertTrue(testFile.withName(newName).path.exists())

		self.assertVerify()


	def test_moveFileBelowBottomLayer(self):
		os.chdir(self.layers[0].path)
		runner = Runner().applyDefaults()
		testFile = self.filesIn(level=-1)[0]
		self.assertFalse(testFile.path.is_symlink())
		runner.run(command=commands.Move, level='down', path=testFile.path)
		self.assertFalse(testFile.path.is_symlink())

	def test_moveFileAboveTopLayer(self):
		os.chdir(self.layers[0].path)
		runner = Runner().applyDefaults()
		testFile = self.filesIn(level=0)[0]
		self.assertFalse(testFile.path.is_symlink())
		runner.run(command=commands.Move, level='up', path=testFile.path)
		self.assertFalse(testFile.path.is_symlink())

	def test_moveFileToSymlinkedDirectory(self):
		from layers.lib import LayerLocalPath
		self.printFsStruct()
		# Find the symlinks that point to a directory
		symdirs:[LayerLocalPath] = self.dirlinks
		# Find the ones that themselves contain a directory
		symdirs = [s for s in symdirs if [p for p in s.path.glob('*') if p.is_dir()]]
		# And a file
		symdirs = [s for s in symdirs if [p for p in s.path.glob('*') if p.is_file()]]
		# Pick any
		symdir = symdirs[0]
		# Fileter for directories
		dirtargets = [t for t in symdir.path.resolve().glob('*') if t.resolve().is_dir()]
		# Fileter for files
		filetargets = [t for t in symdir.path.resolve().glob('*') if t.resolve().is_file()]

		dirtarget = dirtargets[0]
		filetarget = filetargets[0]

		os.chdir(self.layers[0].path)
		runner = Runner().applyDefaults()
		runner.run(command=commands.Move, path=dirtarget, level=symdir.layer.level)
		runner.run(command=commands.Move, path=filetarget, level=symdir.layer.level)
