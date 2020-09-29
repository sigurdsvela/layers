from __future__ import annotations
import os
from pathlib import Path
from typing import Union
from logging import getLogger
from layers.lib import GlobalConsts
from layers.lib import LayerFile
import layers.lib as lib


logger = getLogger()

class Layer:
	def __init__(self, layerSet: 'lib.LayerSet', root: Path):
		from layers.lib import LayerSet
		if not isinstance(root, Path) or not isinstance(layerSet, LayerSet):
			raise TypeError()
		self._layerSet = layerSet
		self._root = root

	@property
	def layerSet(self) -> 'lib.LayerSet':
		return self._layerSet

	@property
	def siblings(self) -> [Layer]:
		return self.layerSet.layers

	def findPurelyDerivativeDirs(self, path=None):
		if path is None:
			path = LayerFile(self, self.root)
		
		derivdirs = []
		dirs = path.listdir(files=False, dirs=True, symlinks=False)
		for d in dirs:
			if len(d.listdir(symlinks=False)) == 0:
				derivdirs.append(d)
			else:
				derivdirs.extend(self.findPurelyDerivativeDirs(d))
		
		return derivdirs


	@property
	def files(self) -> [LayerFile]:
		#All the files in this layer
		_files = []
		for root,dirs,files in os.walk(self.root):
			proot = Path(root)
			for f in files:
				if (proot/f).name != GlobalConsts.LAYER_CONFIG_FILE:
					if not (proot/f).is_symlink():
						_files.append(
							LayerFile(
								layer=self,
								path=(proot/f).relative_to(self.root)
							)
						)
		return _files
	
	@property
	def level(self):
		return self.layerSet.layers.index(self)

	@property
	def root(self):
		return self._root

	# Remove all broken links from this layer
	def purge(self):
		for root, dirs, files in os.walk(self.root):
			paths = files
			paths.extend(dirs)

			paths = [LayerFile(self, Path(root)/p) for p in paths]
			for fpath in paths:
				if fpath.path.is_symlink():
					if not fpath.path.resolve(strict=False).exists():
						fpath.path.unlink()

	def __str__(self) -> str:
		return str(self.root)

	def __eq__(self, other: Layer) -> bool:
		if not isinstance(other, __class__):
			return False
		return self.root.absolute() == other.root.absolute()

__all__ = 'Layer'