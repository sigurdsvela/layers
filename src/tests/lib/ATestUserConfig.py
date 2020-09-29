from pathlib import Path
from testlib.BasicLayerCase import BasicLayerCase
from layers.lib import UserConfig, Layer
from unittest import TestCase
import shutil
import subprocess

class TestUserConfig(TestCase):
	def setUp(self):
		self.config = UserConfig.forCurrentUser()
		self.assertTrue(self.config.path.exists())

	def tearDown(self):
		subprocess.Popen(["rm", "-rf", (self.config.path)]).wait()
		self.assertFalse(self.config.path.exists())

	def test_getsTheRightUser(self):
		self.assertEqual(
			self.config.home,
			Path.home()
		)

	def test_WriteReadConfig(self):
		obj = { 'test': '9905E4F7-0788-4BA0-A366-DABB37EC851E' }
		self.config.writeConfig(obj)
		self.assertEqual(self.config.readConfig(), obj)

	def test_addSetGetLayerSet(self):
		self.assertEqual(len(self.config.layerSets), 0)
		self.config.addLayerSet(name='root')
		self.assertEqual(len(self.config.layerSets), 1)
		
		self.assertIsNotNone(
			self.config.layerSet(withName='root')
		)
	
	def test_getNoneExistentLayerSet(self):
		self.assertIsNone(
			self.config.layerSet(withName='notAlayerset')
		)

	def test_addLayerToSetByName(self):
		layerSet = self.config.addLayerSet(name='root')
		self.assertEqual(len(self.config.layerSets[0].layers), 0)

		self.config.addLayer(
			Layer(layerSet=layerSet, root=Path("/dosent/matter")),
			toSet='root'
		)
		self.assertEqual(len(self.config.layerSets[0].layers), 1)

	def test_addLayerToSetByObject(self):
		layerSet = self.config.addLayerSet(name='root')
		self.assertEqual(len(self.config.layerSets[0].layers), 0)
		self.config.addLayer(
			Layer(layerSet=layerSet, root=Path("/dosent/matter")),
			toSet=layerSet
		)
		self.assertEqual(len(self.config.layerSets[0].layers), 1)

	def test_findLayerByRoot(self):
		testPath = Path("/dosent/matter")
		layerSet = self.config.addLayerSet(name='root')
		self.assertIsNone(self.config.layer(withRoot=testPath))

		self.config.addLayer(
			Layer(layerSet=layerSet, root=Path("/dosent/matter")),
			toSet='root'
		)

		self.assertIsNotNone(self.config.layer(withRoot=testPath))


	def test_findSetByLayer(self):
		testPath = Path("/dosent/matter")
		root = self.config.addLayerSet(name='root')
		t1 = self.config.addLayerSet(name='1')
		t2 = self.config.addLayerSet(name='2')

		testLayer = self.config.addLayer(
			Layer(layerSet=root, root=Path("/dosent/matter")),
			toSet=root
		)

		self.assertIsNotNone(self.config.layerSet(withLayer=testLayer))
		self.assertIsNotNone(self.config.layerSet(withLayer=testPath))
		self.assertEqual(self.config.layerSet(withLayer=testPath), testLayer)


	
