import sys
sys.path.append("./src")

import unittest
import subprocess
import os
from testdir import TEST_DIR
from unittest import TestCase

from GlobalConsts import SET_CONFIG_FILE
from LayerSet import LayerSet


TEST_LEVEL_1 = 'level1'
TEST_LEVEL_2 = 'level2'
TEST_LEVEL_3 = 'level3'

class TestCreateNewSet(TestCase):
	def setUp(self):
		os.chdir(TEST_DIR)
		subprocess.Popen(["layers", "new" , TEST_LEVEL_1])

	def tearDown(self):
		subprocess.Popen(["rm", "-rf" , TEST_LEVEL_1])


	def test_DirectoryWasCreated(self):
		self.assertTrue((TEST_DIR / TEST_LEVEL_1).is_dir())


	def test_LayerConfigFile(self):
		layerSet = LayerSet(TEST_DIR / TEST_LEVEL_1)
		self.assertTrue((TEST_DIR / TEST_LEVEL_1 / SET_CONFIG_FILE).is_file())
		self.assertEqual(layerSet.config.layers, [str(TEST_DIR / TEST_LEVEL_1)])

