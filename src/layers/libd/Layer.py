from __future__ import annotations
import os
from pathlib import Path
from typing import Union
from logging import getLogger

from layers.lib import Exceptions
from layers.lib import GlobalConsts
from layers.lib import LayerConfig
from layers.lib import LayerLocalPath
from layers.lib import Util


logger = getLogger()

class Layer:
	# Starting at some path, walks up the file tree looking
	# for the first instance of a `.layers` configuration directory
	@classmethod
	def findRoot(cls, path: Path):
		# Starts at the given path, and walks up the file tree
		# , terminating at the first directory where it find a `.layer` config directory
		# Returns the reversed String.
		# Parameters:
		# 	path (Path): The start path
		# Raises:
		#   InvalidLayersPathException - If the path given is not uner a .layers directory
		# Returns:
		# 	(path): The root path of the closest layer  
		root_path = path
		while True:
			if (root_path / GlobalConsts.SET_CONFIG_FILE).exists():
				break

			# If we are at root, but have not found the config dir
			if len(root_path.parts) == 1:
				raise Exceptions.NotALayerDirectoryError(f"{path} is not in a layer directory.")

			root_path = root_path.parent
		return root_path


	@classmethod
	def isInLayer(cls, path):
		try:
			cls.findRoot(path)
		except Exceptions.NotALayerDirectoryError:
			return False
		return True
	

	@classmethod
	def createSet(cls, layer: Path):
		if not layer.exists():
			layer.mkdir()
		if not layer.is_dir():
			raise Exception("Tried to create set on file.")
		LayerConfig.create(layer)


	def __init__(self, path: Union[Path, str]):
		if isinstance(path, str):
			path = Path(path)
		
		if not path.exists():
			raise FileNotFoundError(f"Cant create Layer object for a non existent file {path}. Use .create or .createLayer")
		if not path.is_dir():
			raise NotADirectoryError("Cant create Layer object for a path to a file. Must be a directory.")

		self._path = Layer.findRoot(path)
		self._config = LayerConfig(self._path)


	def createLayer(self, layer: Path, level: int = -1):
		if not layer.exists():
			layer.mkdir()
		if not layer.is_dir():
			raise Exception('Can not create layer. Path exist, but is not a directory')
		
		self._config.linkTo(layer)
		self._config.addLayer(layer, level)

	def findPurelyDerivativeDirs(self, path=None):
		if path is None:
			path = LayerLocalPath(self.path)
		
		derivdirs = []
		dirs = path.listdir(files=False, dirs=True, symlinks=False)
		for d in dirs:
			if len(d.listdir(symlinks=False)) == 0:
				derivdirs.append(d)
			else:
				derivdirs.extend(self.findPurelyDerivativeDirs(d))
		
		return derivdirs

	@property
	def level(self):
		return self._config.layers.index(str(self.path))

	@property
	def config(self):
		return self._config

	@property		
	def layers(self) -> __name__:
		return [Layer(path) for path in self.config.layers]

	@property
	def files(self) -> [LayerLocalPath]:
		#All the files in this layer
		_files = []
		for root,dirs,files in os.walk(self.path):
			proot = Path(root)
			for f in files:
				if (proot/f).name != GlobalConsts.LAYER_CONFIG_FILE:
					if not (proot/f).is_symlink():
						_files.append(
							LayerLocalPath(
								layer=self,
								path=(proot/f).relative_to(self.path)
							)
						)
		return _files

	@property
	def path(self):
		return self._path

	def addLayer(self, mount_path):
		pass


	# Remove all broken links from this layer
	def purge(self):
		for root, dirs, files in os.walk(self.path):
			paths = files
			paths.extend(dirs)

			paths = [LayerLocalPath(Path(root)/p) for p in paths]
			for fpath in paths:
				if fpath.path.is_symlink():
					if not fpath.path.resolve(strict=False).exists():
						fpath.path.unlink()

	def __str__(self) -> str:
		return str(self.path)

	def __eq__(self, other: Layer) -> bool:
		if not isinstance(other, __class__):
			return False
		return self.path.absolute().samefile(other.path.absolute())

__all__ = 'Layer'