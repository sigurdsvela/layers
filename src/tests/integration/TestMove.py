import subprocess
import os
from testlib.BasicLayerCase import BasicLayerCase

class TestSyncAndMove(BasicLayerCase):
	def setUp(self):
		super().setUp()
		syncErrors = super().sync()
		if syncErrors:
			raise syncErrors[0]
	
	def test_moveUpDown(self):
		os.chdir(self.layers[0].path)

		testFile = self.filesIn(level=2)[0]
		subprocess.Popen(["layers", "mv", "--up", testFile.path]).wait()
		self.assertTrue(testFile.path.is_symlink())	
		self.assertFalse(testFile.inLayer(layer=self.layers[1]).path.is_symlink())	

		testFile = self.filesIn(level=0)[0]
		subprocess.Popen(["layers", "mv", "--down", testFile.path]).wait()
		self.assertTrue(testFile.path.is_symlink())	
		self.assertFalse(testFile.inLayer(layer=self.layers[1]).path.is_symlink())

		self.assertVerify()
		

	def test_moveTopBottom(self):
		os.chdir(self.layers[0].path)
		
		testFile = self.filesIn(level=-1)[0]
		subprocess.Popen(["layers", "mv", "--top", testFile.path]).wait()
		self.assertTrue(testFile.path.is_symlink())	
		self.assertFalse(testFile.inLayer(layer=self.layers[0]).path.is_symlink())	


		testFile = self.filesIn(level=0)[0]
		subprocess.Popen(["layers", "mv", "--bottom", testFile.path]).wait()
		self.assertTrue(testFile.path.is_symlink())	
		self.assertFalse(testFile.inLayer(layer=self.layers[-1]).path.is_symlink())	

		self.assertVerify()

	def test_renameFile(self):
		os.chdir(self.layers[0].path)

		testFile = self.files[0]
		newName = '46031CAD-C9C0-4E79-9BCA-AF9C876C3EC0'
		subprocess.Popen(["layers", "mv", testFile.localPath, testFile.withName(newName).localPath]).wait()

		self.assertFalse(testFile.path.exists())
		self.assertTrue(testFile.withName(newName).path.exists())

		self.assertVerify()
