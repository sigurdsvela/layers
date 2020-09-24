import sys
sys.path.append("./src")

import unittest
import subprocess
import os
from unittest import TestCase
import TestUtils


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
		self.assertTrue(
			TestUtils.confirmLinkedSet(
				(TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_1_FILE),
				(TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_1_FILE),
				(TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_1_FILE)
			)
		)

		self.assertTrue(
			TestUtils.confirmLinkedSet(
				(TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_2_FILE),
				(TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_2_FILE),
				(TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_2_FILE)
			)
		)

		self.assertTrue(
			TestUtils.confirmLinkedSet(
				(TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_3_FILE),
				(TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_3_FILE),
				(TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_3_FILE)
			)
		)
	
	def test_moveUpDown(self):
		os.chdir(TEST_DIR / TEST_LEVEL_1)
		subprocess.Popen(["layers", "sync"]).wait()

		# Move level_3 file one up
		subprocess.Popen(["layers", "mv", "--up", TEST_LEVEL_3_FILE]).wait()

		# Original should be on level2
		self.assertFalse((TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_3_FILE).is_symlink())
		# Check symlinks
		self.assertTrue(
			TestUtils.confirmLinkedSet(
				(TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_3_FILE),
				(TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_3_FILE),
				(TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_3_FILE)
			)
		)

		# Move level_1 file one down
		# subprocess.Popen(["layers", "-l", TEST_DIR / TEST_LEVEL_1, "mv", "--down", TEST_LEVEL_1]).wait()

		# # Original should be on level2
		# self.assertFalse((TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_1_FILE).is_symlink())
		# # Check symlinks
		# self.assertTrue(
		# 	TestUtils.confirmLinkedSet(
		# 		(TEST_DIR / TEST_LEVEL_1 / TEST_LEVEL_1_FILE),
		# 		(TEST_DIR / TEST_LEVEL_2 / TEST_LEVEL_1_FILE),
		# 		(TEST_DIR / TEST_LEVEL_3 / TEST_LEVEL_1_FILE)
		# 	)
		# )


