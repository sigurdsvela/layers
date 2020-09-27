import sys
import unittest
import subprocess
import os
from tests.testconst import TEST_DIR, TEST_LEVEL_1, TEST_LEVEL_2, TEST_LEVEL_3
from unittest import TestCase
from BasicLayerCase import BasicLayerCase


from layers.lib import GlobalConsts as GC
from layers.lib import Layer
from layers.lib import LayerLocalPath

class TestPurge(BasicLayerCase):
	def setUp(self):
		super().setUp()
		self.assertTrue(len(super().sync()) == 0, "Sync failed")

	def test_Purge(self):
		files = super().files
		
		layers = self.layers
		filesRemoved: LayerLocalPath = []

		# Remove about half of original files
		for file in files[0:len(files)//2]:
			filesRemoved.append(file)
			file.path.unlink()

		# Convirm their removal, and the precence of the (now broken) symlinks
		for layer in layers:
			for file in filesRemoved:
				if (f := file.inLayer(layer).path).exists():
					self.assertTrue(f.is_symlink())
					self.assertFalse(f.resolve(strict=False).exists())

		# Confirm that there are errors now
		self.assertGreater(len(super().verify()), 0)
		# Run purge
		subprocess.Popen(["layers", "-v", "-l", self.layers[0].path, "purge"]).wait()
		# Confirm that we fixed all the errors
		errors = super().verify()
		self.assertEqual(len(errors), 0, errors)
