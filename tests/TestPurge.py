import sys
import unittest
import subprocess
import os
from testconst import TEST_DIR, TEST_LEVEL_1, TEST_LEVEL_2, TEST_LEVEL_3
from unittest import TestCase
from BasicLayerCase import BasicLayerCase
from GlobalConsts import SET_CONFIG_FILE
from Layer import Layer
from LayerLocalPath import LayerLocalPath

class TestPurge(BasicLayerCase):
	def setUp(self):
		super().setUp()
		self.assertTrue(len(super().sync()) == 0, "Sync failed")

	def tearDown(self):
		super().tearDown()

	def test_Purge(self):
		files = super().files()
		
		layers = self.layers
		filesRemoved = []

		# Remove about half of original files
		for file in files[0:len(files)//2]:
			filesRemoved.append(file)
			file.fullPath.unlink()

		# Convirm their removal, and the precence of the (now broken) symlinks
		for layer in layers:
			for file in filesRemoved:
				if (layer/file.path).exists():
					self.assertTrue((layer/file.path).is_symlink())
					self.assertFalse((layer/file.path).resolve(strict=False).exists())

		# Confirm that there are errors now
		self.assertGreater(len(super().verify()), 0)
		# Run purge
		subprocess.Popen(["layers", "-v", "-l", self.layers[0], "purge"]).wait()
		# Confirm that we fixed all the errors
		errors = super().verify()
		self.assertEqual(len(errors), 0, errors)
