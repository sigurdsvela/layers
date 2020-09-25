from pathlib import Path
from Layer import Layer

# Represents a set of layers in a layer set
class LayerSet:
	@classmethod
	def fromLayer(cls, layer: Layer):
		return cls(layer.config.path.resolve())

	def __init__(self, baseLayer: Layer):
		self.baseLayer = baseLayer

	# Remove a file (or directory) from the entire layer set
	def rm(self, lpath: Path):
		pass

	# Sync the entire layer set
	def sync(self):
		pass

	# Purge the entire layer set
	def purge(self):
		for layerPath in self.baseLayer.layers:
			Layer(layerPath).purge()

	# Merge layerset into target and remove the layers (Except the target)
	def merge(self, target: Path):
		pass