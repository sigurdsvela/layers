from testlib.BasicLayerCase import BasicLayerCase

class TestBasicLayerCase(BasicLayerCase):
	def setUp(self):
		super().setUp()
		self.sync()

	def test_Setup(self):
		from layers.lib import LayerSet

		self.assertCountEqual(self.verify(), [])
		self.assertCountEqual(LayerSet.fromLayer(self.layers[0]).layers, self.layers)
