# A path, containing, as seperate parts, the layer root, and the path relative to that root
from pathlib import Path
from typing import Union

class LayerLocalPath:
	
	def _fromPath(self, path: Path):
		from layers.lib import Layer
		self._layerPath = Layer.findRoot(path)
		self._localPath = path.absolute().relative_to(self._layerPath)

	def _fromLayerAndPath(self, layer: Path, path: Path):
		from layers.lib import Layer
		self._layerPath = Layer.findRoot(layer)
		self._localPath = path

	
	def __init__(self, path:Union[Path,str], layer:Union[Path,str] = None):
		from layers.lib import Layer

		if layer is None:
			if isinstance(path, Path):
				self._fromPath(path)
			elif isinstance(path, str):
				self._fromPath(Path(path))
			else:
				raise TypeError("Unknown signature")
		else:
			if isinstance(layer, str):
				layer = Path(layer)

			if isinstance(layer, Layer):
				layer = layer.path

			if isinstance(path, str):
				path = Path(path)

			if isinstance(path, Path) and isinstance(layer, Path):
				self._fromLayerAndPath(layer, path)
			else:
				raise TypeError("Uknown Signature")

	def inLayer(self, layer: Union[Path]):
		from layers.lib import Layer

		if isinstance(layer, Layer):
			return LayerLocalPath(layer=layer.path, path=self.localPath)
		elif isinstance(layer, Path):
			return LayerLocalPath(layer=layer, path=self.localPath)
		else:
			raise TypeError("Invalid signature")

	def inLevel(self, level:int):
		return LayerLocalPath(layer=self.layer.layers[level], path=self.localPath)

	def withName(self, name: str):
		return LayerLocalPath(layer=self.layerPath, path=self.localPath.parent / name)

	def withLocalPath(self, localPath: Path):
		return LayerLocalPath(layer=self.layerPath, path=localPath)

	@property
	def isRoot(self):
		return len(self.localPath.parts) == 0

	@property
	def parent(self):
		if self.isRoot:
			return None
		return self.withLocalPath(self.localPath.parent)

	@property
	def layer(self):
		from layers.lib import Layer
		return Layer(self._layerPath)

	@property
	def layerPath(self) -> Path:
		return self._layerPath

	@property
	def localPath(self) -> Path:
		return self._localPath

	@property
	def path(self) -> Path:
		return self.layerPath / self.localPath

	def __str__(self) -> str:
		return str(self.layerPath / self.localPath)
