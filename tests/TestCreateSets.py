import sys
sys.path.append("./src")

import unittest
import subprocess
import os
from testconst import TEST_DIR, TEST_LEVEL_1, TEST_LEVEL_2, TEST_LEVEL_3
from unittest import TestCase

from GlobalConsts import SET_CONFIG_FILE
from Layer import Layer



class TestCreateNewSet(TestCase):
	def setUp(self):
		os.chdir(TEST_DIR)
		subprocess.Popen(["layers", "new" , TEST_LEVEL_1]).wait()

	def tearDown(self):
		subprocess.Popen(["rm", "-rf" , TEST_LEVEL_1]).wait()


	def test_DirectoryWasCreated(self):
		self.assertTrue((TEST_DIR / TEST_LEVEL_1).is_dir())


	def test_LayerConfigFile(self):
		layer = Layer(TEST_DIR / TEST_LEVEL_1)
		self.assertTrue((TEST_DIR / TEST_LEVEL_1 / SET_CONFIG_FILE).is_file())
		self.assertEqual(layer.config.layers, [str(TEST_DIR / TEST_LEVEL_1)])

