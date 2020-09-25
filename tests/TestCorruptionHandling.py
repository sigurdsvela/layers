import sys
from unittest import TestCase
import unittest
import subprocess
import os
import TestUtils
from testconst import *
import GlobalConsts
from Layer import Layer

class TestCorruptionHandling(TestCase):
	def setUp(self):
		subprocess.Popen(["rm", "-rf", TEST_DIR]).wait()
		TEST_DIR.mkdir(mode=0o775, parents=True)
		os.chdir(TEST_DIR)

		# Create 3 layers
		subprocess.Popen(["layers", "new", TEST_DIR / TEST_LEVEL_1]).wait()
		subprocess.Popen(["layers", "-l", TEST_DIR / TEST_LEVEL_1, "new", TEST_DIR / TEST_LEVEL_2]).wait()
		subprocess.Popen(["layers", "-l", TEST_DIR / TEST_LEVEL_1, "new", TEST_DIR / TEST_LEVEL_3]).wait()

		# Create files
		(TEST_DIR / L1 / L1_FILE).touch()
		(TEST_DIR / L2 / L2_FILE).touch()
		(TEST_DIR / L3 / L3_FILE).touch()

		subprocess.Popen(["layers", "-l", TEST_DIR / TEST_LEVEL_1, "sync"]).wait()

	def tearDown(self):
		subprocess.Popen(["rm", "-rf", TEST_DIR]).wait()

	# If a symlink is missing, it should just be created
	def test_missingSymlink(self):
		# Remove a synlink
		(TEST_DIR / L1 / L2_FILE).unlink()
		self.assertFalse((TEST_DIR / L1 / L2_FILE).exists())
		# Resync
		subprocess.Popen(["layers", "-l", TEST_DIR / TEST_LEVEL_1, "sync"]).wait()
		# Check the links
		self.assertTrue(TestUtils.confirmLinkedSet(
			(TEST_DIR / L1 / L2_FILE),
			(TEST_DIR / L2 / L2_FILE),
			(TEST_DIR / L3 / L2_FILE)
		))

	def test_missingOriginal(self):
		#Remove a synlink
		(TEST_DIR / L1 / L1_FILE).unlink()
		self.assertFalse((TEST_DIR / L1 / L1_FILE).exists())
		# Resync
		devnull = Path("/dev/null")
		devnullw = devnull.open('w')
		(p := subprocess.Popen(
			["layers", "-l", TEST_DIR / TEST_LEVEL_1, "sync"],
			stdout = devnullw,
			stderr = devnullw
		)).wait()
		devnullw.close()

		# Expect be done
		self.assertFalse(p.returncode is None)
		# But expect faileure
		self.assertFalse(p.returncode == 0)

		# Check remainding links
		self.assertTrue(TestUtils.confirmLinkedSet(
			(TEST_DIR / L1 / L2_FILE),
			(TEST_DIR / L2 / L2_FILE),
			(TEST_DIR / L3 / L2_FILE)
		))
		self.assertTrue(TestUtils.confirmLinkedSet(
			(TEST_DIR / L1 / L3_FILE),
			(TEST_DIR / L2 / L3_FILE),
			(TEST_DIR / L3 / L3_FILE)
		))
