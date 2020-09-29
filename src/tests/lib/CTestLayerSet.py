from unittest import TestCase
from layers.lib import LayerSet, UserConfig, Layer
from pathlib import Path
import shutil


class TestLayerSet(TestCase):
	def setUp(self):
		self.config = UserConfig.forCurrentUser()
		self.rootSet = self.config.addLayerSet(name='root')

		self.layers = []
		self.layers.extend(self.config.addLayer(
			layer=Layer(layerSet=self.rootSet, root=Path('~/test-layer1')),
			toSet=self.rootSet
		))

		self.layers.extend(self.config.addLayer(
			layer=Layer(layerSet=self.rootSet, root=Path('~/test-layer2')),
			toSet=self.rootSet
		))

		self.layers.extend(self.config.addLayer(
			layer=Layer(layerSet=self.rootSet, root=Path('~/test-layer3')),
			toSet=self.rootSet
		))

		for layer in self.layers:
			layer.root.mkdir()

	def tearDown(self):
		shutil.rmtree(self.config.path)
		for layer in self.layers:
			shutil.rmtree(layer.root)
