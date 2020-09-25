# A path, containing, as seperate parts, the layer root, and the path relative to that root

from pathlib import Path


class LayerLocalPath:

	def __init__(self, layer: Path, path: Path):
		self._layer = layer
		self._path = path

	@property
	def layer(self):
		return self._layer

	@property
	def path(self):
		return self._path

	@property
	def fullPath(self):
		return self.layer / self.path


	
