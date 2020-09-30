from testlib.LayersLibTestCase import LayersLibTestCase
from layers.lib import LayerSet, UserConfig, Layer, LayerFile, Level
from pathlib import Path
import shutil
import subprocess

class TestLayerSet(LayersLibTestCase):
	def setUp(self):
		self.config = UserConfig.forCurrentUser()
		subprocess.Popen(["rm", "-rf", (self.config.path)]).wait()
		self.config = UserConfig.forCurrentUser()

		self.config = UserConfig.forCurrentUser()
		self.rootSet = self.config.addLayerSet(name='root')

		self.layers = []
		self.layers.extend([self.config.addLayer(
			layer=Layer(layerSet=self.rootSet, root=Path('~/test-layer1').expanduser()),
			toSet=self.rootSet
		)])

		self.layers.extend([self.config.addLayer(
			layer=Layer(layerSet=self.rootSet, root=Path('~/test-layer2').expanduser()),
			toSet=self.rootSet
		)])

		self.layers.extend([self.config.addLayer(
			layer=Layer(layerSet=self.rootSet, root=Path('~/test-layer3').expanduser()),
			toSet=self.rootSet
		)])

		for layer in self.layers:
			if layer.root.exists():
				subprocess.Popen(["rm", "-rf", layer.root]).wait()
			layer.root.mkdir()

		self.maxDiff = None

	def tearDown(self):
		shutil.rmtree(self.config.path)
		for layer in self.layers:
			shutil.rmtree(layer.root)

	def test_Equality(self):
		path = Path("/dosent/matter")
		this = LayerSet(config=self.config, name='root')
		other = LayerSet(config=self.config, name='root')
		self.assertEqual(this, other)
		other = LayerSet(config=self.config, name='not-root')
		self.assertNotEqual(this, other)

	def test_argumentParser(self):
		parse = LayerSet.parseFactory(config=self.config, cwd=Path.cwd())
		self.assertEqual(parse('root'), self.rootSet)
		parse = LayerSet.parseFactory(config=self.config, cwd=self.layers[0].root)
		self.assertEqual(parse(''), self.rootSet)

	def test_exists(self):
		self.assertTrue(self.rootSet.exists())
		self.assertFalse(LayerSet(config=self.config, name='noop').exists())

	def test_findLayerFile(self):
		path = Path("/dosent/exists")
		self.assertIsNone(
			self.rootSet.findLayerFile(path)
		)

		path = Path(self.layers[0].root / "testfile")
		layerFile = LayerFile(layer=self.layers[0], path=path.relative_to(self.layers[0].root))
		path.touch()
		self.assertEqual(
			self.rootSet.findLayerFile(path),
			layerFile
		)

	def test_name(self):
		self.assertEqual(self.rootSet.name, 'root')

	def test_config(self):
		self.assertEqual(self.rootSet.config, self.config)

	def test_layers(self):
		self.assertUnorderedListsEqual(self.rootSet.layers, self.layers)

	def test_files(self):
		testFile = "testfile"

		files = []
		for layer in self.layers:
			f = (layer.root/f"{testFile}-{layer.level}")
			f.touch()
			files.extend([LayerFile(layer=layer, path=f.relative_to(layer.root))])

		self.assertUnorderedListsEqual(self.rootSet.findFiles(), files)

	def test_dirs(self):
		testFile = "testdir"
		for layer in self.layers:
			(layer.root/testFile).mkdir()

		dirs = []
		for layer in self.layers:
			dirs.extend([LayerFile(layer=layer, path=Path(testFile))])

		self.assertUnorderedListsEqual(dirs, self.rootSet.findDirs())

	def test_addLayerAtTop(self):
		from layers.lib import Level
		from pprint import pprint
		layerRoot = Path("/dosent/matter")
		testLayer = Layer(layerSet=self.rootSet, root=layerRoot)
		self.rootSet.addLayer(testLayer, atLevel=Level.TOP)
		self.assertEqual(self.rootSet.layers[0], testLayer)

	def test_addLayerAtBottom(self):
		from layers.lib import Level
		layerRoot = Path("/dosent/matter")
		testLayer = Layer(layerSet=self.rootSet, root=layerRoot)
		self.rootSet.addLayer(testLayer, atLevel=Level.BOTTOM)
		self.assertEqual(self.rootSet.layers[-1], testLayer)

	def test_addLayerAtIndex(self):
		from layers.lib import Level
		layerRoot = Path("/dosent/matter")
		testLayer = Layer(layerSet=self.rootSet, root=layerRoot)
		self.rootSet.addLayer(testLayer, atLevel=Level(1))
		self.assertEqual(self.rootSet.layers[1], testLayer)

	def test_simpleSync(self):
		from layers.lib import Level
		testFile = LayerFile(self.layers[0], Path("test-file"))
		testFile.absolute.touch()
		
		self.rootSet.sync()

		for layer in self.rootSet.layers:
			self.assertFileExist(testFile.inLayer(layer))
		for layer in self.rootSet.layers:
			if layer != self.layers[0]:
				self.assertTrue(testFile.inLayer(layer).isSymlink())
				self.assertEqual(testFile.inLayer(layer).origin, testFile)

	def test_syncWithSubdir(self):
		# TODO
		pass

	def test_syncWithShareSubdir(self):
		# TODO
		pass

	def test_simpleMoveFile(self):
		# TODO
		pass

	def test_moveFileToLinkedDirectory(self):
		# TODO
		pass

	def test_simpleMoveDirectory(self):
		# TODO
		pass

	def test_simpleMoveMergeDirectory(self):
		# TODO
		pass

	def test_syncRemovesSimpleDerivativeDirectories(self):
		# TODO
		pass

	def test_syncRemovesRecursiveDerivativeDirectories(self):
		# TODO
		pass
	