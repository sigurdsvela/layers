from testlib.BasicLayerCase import BasicLayerCase
from layers.cli import Runner

class TestSync(BasicLayerCase):
	def setUp(self):
		super().setUp()
		self.sync()

	def test_purelyDerivativeDirectoryHandling(self):
		from layers.cli import commands
		runner = Runner().applyDefaults().quiet()

		dirs = self.dirlinks
		dirs = [d for d in dirs if len(d.origin.listdir()) >= 2]
		d = dirs[0]
		testFile = d.origin.listdir()[0]
		originLayer = testFile.layer
		# Take one file from the directory and move it to the symlinked directory
		try:
			testFile.origin.move(inLayer=d.layer)
			# Confirm that it is not not a symlink
			self.assertFalse(d.isSymlink())
			# Move it back
			testFile.origin.move(inLayer=originLayer)
			# The directory is still not a symlink
			# But now contains no files
			self.assertFalse(d.isSymlink())
			# But now, if we sync, the sync function should
			# be able to recognize the fact that the directory
			# can be removed and replaced with a single symlink
			runner.run(command=commands.Sync, target_layer=self.layers[0].path)
			self.assertTrue(d.isSymlink())
		except Exception as e:
			self.printFsStruct()
			raise e


