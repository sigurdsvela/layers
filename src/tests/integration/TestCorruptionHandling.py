import subprocess
import os

from layers.cli import Runner, commands
from testlib.BasicLayerCase import BasicLayerCase

class TestCorruptionHandling(BasicLayerCase):
	def setUp(self):
		super().setUp()
		super().sync()
		super().assertVerify()

	def test_missingSymlink(self):
		os.chdir(self.layers[0].path)
		runner = Runner().quiet().applyDefaults()

		#There should be no problems
		file = self.filesIn(level=0)[0]

		# Remove a symlink
		file.inLevel(1).path.unlink()

		# Confirm the error
		self.assertTrue(self.verify())

		# Run sync
		runner.run(command=commands.Sync)

		# The error is gone
		self.assertFalse(self.verify())

	def test_missingOriginal(self):
		os.chdir(self.layers[0].path)
		runner = Runner().quiet().applyDefaults()

		#There should be a problem
		file = self.filesIn(level=0)[0]

		# Remove the original
		file.path.unlink()

		# Confirm the error
		self.assertTrue(self.verify())

		# Purge
		runner.run(command=commands.Purge)

		# Error running sync
		self.assertFalse(self.verify())
