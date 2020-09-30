from testlib.LayersLibTestCase import LayersLibTestCase
from pathlib import Path
from layers.lib import Level

class TestLevel(LayersLibTestCase):
	def test_index(self):
		for number in range(0, 1000, 10):
			self.assertEqual(int(Level(number)), number)

	def test_basicOffsett(self):
		for number in range(0, 1000, 10):
			for offset in range(-1000, 1000, 10):
				self.assertEqual(int(Level(number)+offset), number+offset)
	
	def test_topAndBottomForEmptySet(self):
		lset = self.config.addLayerSet(name='root')
		self.assertEqual(int(Level.TOP(lset)), 0)
		self.assertEqual(int(Level.BOTTOM(lset)), 0)

	def test_topAndBottomForNonEmptySet(self):
		lset = self.config.addLayerSet(name='root')
		lset.addLayer(layer=Path("/layer1"))
		lset.addLayer(layer=Path("/layer2"))
		lset.addLayer(layer=Path("/layer3"))
		self.assertEqual(int(Level.TOP(lset)), 0)
		self.assertEqual(int(Level.BOTTOM(lset)), 2)

	def test_upDownForTopLayer(self):
		lset = self.config.addLayerSet(name='root')
		layer = lset.addLayer(layer=Path("/layer1"))
		lset.addLayer(layer=Path("/layer2"))
		lset.addLayer(layer=Path("/layer3"))
		self.assertEqual(int(Level.UP(layer)), 0)
		self.assertEqual(int(Level.DOWN(layer)), 1)
	
	def test_upDownForBottomLayer(self):
		lset = self.config.addLayerSet(name='root')
		lset.addLayer(layer=Path("/layer1"))
		lset.addLayer(layer=Path("/layer2"))
		layer = lset.addLayer(layer=Path("/layer3"))
		self.assertEqual(int(Level.UP(layer)), 1)
		self.assertEqual(int(Level.DOWN(layer)), 2)

	def test_upDownForMiddleLayer(self):
		lset = self.config.addLayerSet(name='root')
		lset.addLayer(layer=Path("/layer1"))
		layer = lset.addLayer(layer=Path("/layer2"))
		lset.addLayer(layer=Path("/layer3"))
		self.assertEqual(int(Level.UP(layer)), 0)
		self.assertEqual(int(Level.DOWN(layer)), 2)

	def test_upDownForLayerSetAsTarget(self):
		lset = self.config.addLayerSet(name='root')
		lset.addLayer(layer=Path("/layer1"))
		lset.addLayer(layer=Path("/layer2"))
		lset.addLayer(layer=Path("/layer3"))
		self.assertEqual(int(Level.UP(lset)), 0)
		self.assertEqual(int(Level.DOWN(lset)), 0)

	def test_offset(self):
		lset = self.config.addLayerSet(name='root')
		lset.addLayer(layer=Path("/layer0"))
		layer1 = lset.addLayer(layer=Path("/layer1"))
		lset.addLayer(layer=Path("/layer2"))

		self.assertEqual(int(Level.DOWN(layer1)-1), 1)
		self.assertEqual(int(Level.UP(layer1)+1), 1)
		self.assertEqual(int(Level.UP(layer1)-1), -1)
		self.assertEqual(int(Level.DOWN(layer1)+1), 3)

		self.assertEqual(int(Level.TOP(layer1)+1), 1)
		self.assertEqual(int(Level.BOTTOM(layer1)-1), 1)
		self.assertEqual(int(Level.TOP(layer1)-1), -1)
		self.assertEqual(int(Level.BOTTOM(layer1)+1), 3)


