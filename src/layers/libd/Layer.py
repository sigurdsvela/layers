from __future__ import annotations
import os
from pathlib import Path
from typing import Union
from logging import getLogger
import layers.lib as lib


logger = getLogger()

class Layer:
	def __init__(self, layerSet: lib.LayerSet, root: Path):
		from layers.lib import LayerSet
		if not isinstance(root, Path) or not isinstance(layerSet, LayerSet):
			raise TypeError()
		self._layerSet = layerSet
		self._root = root

	@property
	def layerSet(self) -> lib.LayerSet:
		return self._layerSet

	@property
	def siblings(self) -> [Layer]:
		return self.layerSet.layers

	def findPurelyDerivativeDirs(self, path=None) -> [LayerFile]:
		from layers.lib import LayerFile
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


	def findFiles(self, withFilter: callable = lambda f: f.is_file() and not f.is_symlink()) -> [LayerFile]:
		from layers.lib import GlobalConsts, LayerFile
		#All the files in this layer
		_files = []
		for root,dirs,files in os.walk(self.root):
			proot = Path(root)
			for f in files:
				if withFilter(proot/f):
					_files.append(
						LayerFile(
							layer=self,
							path=(proot/f).relative_to(self.root)
						)
					)
		return _files

	def findDirs(self, withFilter: callable = lambda x: x) -> [LayerFile]:
		from layers.lib import GlobalConsts, LayerFile
		#All the files in this layer
		_files = []
		for root,dirs,files in os.walk(self.root):
			proot = Path(root)
			for f in dirs:
				if withFilter(proot/f):
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
		from layers.lib import LayerFile
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
			raise TypeError(f"Layer == {type(other)} not supported")
		return self.root.absolute() == other.root.absolute()

__all__ = 'Layer'