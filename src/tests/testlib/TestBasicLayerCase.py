from testlib.BasicLayerCase import BasicLayerCase

class TestBasicLayerCase(BasicLayerCase):
	def setUp(self):
		super().setUp()
		self.sync()

	def test_Setup(self):
		from layers.lib import LayerSet, UserConfig

		self.assertCountEqual(self.verify(), [])
		self.assertCountEqual(self.testLayerSet.layers, self.layers)
