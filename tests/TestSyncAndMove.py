import sys
sys.path.append("./src")

import unittest
import subprocess
import os
from unittest import TestCase

from GlobalConsts import SET_CONFIG_FILE
from LayerSet import LayerSet

from testconst import (
	TEST_DIR,
	TEST_LEVEL_1,
	TEST_LEVEL_2,
	TEST_LEVEL_3,
	TEST_LEVEL_1_FILE,
	TEST_LEVEL_2_FILE,
	TEST_LEVEL_3_FILE
)

class TestSyncAndMove(TestCase):
	def setUp(self):
		subprocess.Popen(["rm", "-rf", TEST_DIR]).wait()
		TEST_DIR.mkdir(mode=0o775, parents=True)
		os.chdir(TEST_DIR)

		# Create 3 layers
		subprocess.Popen(["layers", "new", TEST_DIR / TEST_LEVEL_1]).wait()
		subprocess.Popen(["layers", "-l", TEST_DIR / TEST_LEVEL_1, "new", TEST_DIR / TEST_LEVEL_2]).wait()
		subprocess.Popen(["layers", "-l", TEST_DIR / TEST_LEVEL_1, "new", TEST_DIR / TEST_LEVEL_3]).wait()

		# Create files
		(TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_1_FILE).touch()
		(TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_2_FILE).touch()
		(TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_3_FILE).touch()


	def tearDown(self):
		subprocess.Popen(["rm", "-rf", TEST_DIR]).wait()

	def test_Setup(self):
		self.assertTrue(TEST_DIR.is_dir())
		self.assertTrue((TEST_DIR / TEST_LEVEL_1).is_dir())
		self.assertTrue((TEST_DIR / TEST_LEVEL_2).is_dir())
		self.assertTrue((TEST_DIR / TEST_LEVEL_3).is_dir())
		self.assertTrue((TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_1_FILE).is_file())
		self.assertTrue((TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_2_FILE).is_file())
		self.assertTrue((TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_3_FILE).is_file())

	def test_Sync(self):
		subprocess.Popen(["layers", "-l", TEST_DIR / TEST_LEVEL_1, "sync"]).wait()
		# File preservation
		self.assertTrue((TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_1_FILE).is_file())
		self.assertTrue((TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_2_FILE).is_file())
		self.assertTrue((TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_3_FILE).is_file())

		# Synlink creation
		self.assertTrue((TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_2_FILE).is_symlink())
		self.assertEqual(
			(TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_2_FILE).resolve().absolute(),
			(TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_2_FILE).resolve().absolute()
		)
		self.assertTrue((TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_3_FILE).is_symlink())
		self.assertEqual(
			(TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_3_FILE).resolve().absolute(),
			(TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_3_FILE).resolve().absolute()
		)
		self.assertTrue((TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_1_FILE).is_symlink())
		self.assertEqual(
			(TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_1_FILE).resolve().absolute(),
			(TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_1_FILE).resolve().absolute()
		)
		self.assertTrue((TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_3_FILE).is_symlink())
		self.assertEqual(
			(TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_3_FILE).resolve().absolute(),
			(TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_3_FILE).resolve().absolute()
		)
		self.assertTrue((TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_1_FILE).is_symlink())
		self.assertEqual(
			(TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_1_FILE).resolve().absolute(),
			(TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_1_FILE).resolve().absolute()
		)
		self.assertTrue((TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_2_FILE).is_symlink())
		self.assertEqual(
			(TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_2_FILE).resolve().absolute(),
			(TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_2_FILE).resolve().absolute()
		)

		
