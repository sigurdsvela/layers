# A path, containing, as seperate parts, the layer root, and the path relative to that root
from __future__ import annotations
from pathlib import Path
from typing import Union
import os

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

	def getLocalParent(self):
		# Get the parent of this files that
		# exists in the same layer (is not symlinked)
		parent = self.parent
		while parent.origin.layer != self.layer:
			parent = parent.parent
		return parent

	def stepTowards(self, path):
		steps = path.localPath.relative_to(self.localPath).parts
		return self/steps[0]

	def move(self, *args, **kwargs):
		if len(args) == 1:
			self.moveToPathAndLayer(args[0].localPath, args[0].layer)
		elif 'withLocalPath' in kwargs or 'inLayer' in kwargs:
			self.moveToPathAndLayer(
				kwargs['withLocalPath'] if 'withLocalPath' in kwargs else None,
				kwargs['inLayer'] if 'inLayer' in kwargs else None
			)
		else:
			raise TypeError("Invalid function signature")

	def moveToPathAndLayer(self, withLocalPath=None, inLayer=None):
		# Moves the origin file to a new path and layer
		import logging
		logger = logging.getLogger(".".join([__name__, __file__, str(__class__), "move"]))

		# Nothing specified, nothing ot do
		if withLocalPath is None and inLayer is None:
			logger.debug("both path and layer argument was empty. Nothing to do.")
			return self

		path = withLocalPath if withLocalPath is not None else self.localPath
		targetLayer = inLayer if inLayer is not None else self.layer
		newOrigin = self.inLayer(targetLayer).withLocalPath(path)
		origin = self.origin
		logger.debug(f"target:{origin}, new local path:{path}, new layer: {targetLayer.path}")
		logger.debug(f"origin:{origin}, newOrigin:{newOrigin}")

		if origin == newOrigin:
			logger.debug("New location same as previos")
			return

		# Check that the target location is not occupied
		if newOrigin.exists() and newOrigin.isOrigin():
			raise FileExistsError(f"Cannot move file {origin} to {newOrigin}. File exists.")

		# Check that the directory structure
		# exists in the target layer (Is not just symlinked)
		localParent = newOrigin.getLocalParent()
		linked = localParent.stepTowards(newOrigin)
		assert(linked.isSymlink() or not linked.exists())
		if linked.isDir():
			logger.debug("Target origin path was symlinked. Creating directory structure")
			logger.debug(f"- unlink {linked}")
			linked.unlink()
			logger.debug(f"- mkdir {linked}")
			linked.path.mkdir(parents=True, exist_ok=True)

		logger.debug("Removing links to the previous origin file")
		# Remove links to the origin file
		for layer in self.layer.layers:
			if origin.inLayer(layer).isSymlink():
				origin.inLayer(layer).unlink()

		# Move the file
		logger.debug("Moving the file to the spesified location.")
		self.origin.path.rename(newOrigin.path)

		# Create the new links
		logger.debug("Creating links to the new origin file")
		for layer in self.layer.layers:
			if layer != newOrigin.layer:
				newOrigin.inLayer(layer).symlinkTo(newOrigin.layer)
		logger.debug("Done.")
		return newOrigin

	def listdir(self, files=True, dirs=True, symlinks=True):
		if not self.isDir():
			raise NotADirectoryError("")

		dirList = [
			__class__(self.path / p) for p in os.listdir(self.path)
		]

		if not files:
			dirList = [p for p in dirList if not p.isFile()]
		
		if not dirs:
			dirList = [p for p in dirList if not p.isDir()]
		
		if not symlinks:
			dirList = [p for p in dirList if not p.isSymlink()]

		return dirList

	def isDir(self):
		return self.path.resolve().is_dir()

	def isFile(self):
		return self.path.is_file()

	def isSymlink(self):
		return self.path.is_symlink()

	def isOrigin(self):
		return self.origin.layer == self.layer

	def unlink(self, force=False):
		from layers.lib import Exceptions
		# Unlink a file.
		# Raises an exception if 
		# The file is the original, and the
		# force argument is not set to true
		if not self.isSymlink() and not force:
			raise Exceptions.UnsafeOnOriginalError("Tried to unlink an origin file, without the 'force' arg set")
		self.path.unlink()

	def symlinkTo(self, layer):
		self.path.symlink_to(self.inLayer(layer).path)

	def relativeTo(self, path: LayerLocalPath):
		return LayerLocalPath(self.path.relative_to(path.path))

	def rmdir(self):
		return self.path.rmdir()

	def exists(self):
		return self.path.exists()

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
	def origin(self):
		return LayerLocalPath(self.path.resolve(strict=False).absolute())

	@property
	def layerPath(self) -> Path:
		return self._layerPath

	@property
	def localPath(self) -> Path:
		return self._localPath

	@property
	def path(self) -> Path:
		return self.layerPath / self.localPath

	def __eq__(self, other:LayerLocalPath):
		if not self.layerPath == other.layerPath:
			return False
		if not self.localPath == other.localPath:
			return False
		return True

	def __str__(self) -> str:
		return str(self.layerPath / self.localPath)

	def __truediv__(self, other:Union[Path, str]):
		return self.withLocalPath(self.localPath/other)
