# A path, containing, as seperate parts, the layer root, and the path relative to that root
from __future__ import annotations
from pathlib import Path
from typing import Union
import layers.lib as lib
import os
import shutil

class LayerFile:
	@classmethod
	def parserFactory(cls, layerSet: lib.LayerSet):
		return lambda arg: cls.parse(arg, layerSet)

	@classmethod
	def parse(cls, arg, layerSet: lib.LayerSet):
		from layers.lib import Exceptions
		path = Path(arg).absolute()

		layerFile = layerSet.findLayerFile(path)

		if layerFile is None:
			return Exceptions.InvalidArgumentError(argType="LayerFile", argValue=arg)
		else:
			return LayerFile(layerSet, path)

	def __init__(self, layer: lib.Layer, path: Path):
		from layers.lib import Layer
		if not isinstance(path, Path) or not isinstance(layer, Layer):
			raise TypeError()
		self._layer = layer
		self._path = path

	def inLayer(self, layer: Layer):
		from layers.lib import Layer
		return LayerFile(layer, self._path)

	def inLevel(self, level:int):
		return LayerFile(layer=self.layer.layerSet.layers[level], path=self.path)

	def withName(self, name: str):
		return LayerFile(layer=self.layer, path=self.path.parent / name)

	def withPath(self, path: Path):
		return LayerFile(layer=self.layer, path=path)

	def getLocalParent(self):
		# Get the parent of this files that
		# exists in the same layer (is not symlinked)
		parent = self.parent
		while parent.origin.layer != self.layer:
			parent = parent.parent
		return parent

	def stepTowards(self, path):
		steps = path.localPath.relative_to(self.path).parts
		return self/steps[0]

	def move(self, *args, **kwargs):
		if len(args) == 1:
			self.moveToPathAndLayer(args[0].path, args[0].layer)
		elif 'withPath' in kwargs or 'inLayer' in kwargs:
			self.moveToPathAndLayer(
				kwargs['withPath'] if 'withPath' in kwargs else None,
				kwargs['inLayer'] if 'inLayer' in kwargs else None
			)
		else:
			raise TypeError("Invalid function signature")


	def moveToPathAndLayer(self, path=None, layer=None):
		from layers.lib import Exceptions

		# Moves the origin file to a new path and layer
		import logging
		logger = logging.getLogger(".".join([__name__, __file__, str(__class__), "move"]))

		# Nothing specified, nothing ot do
		if path is None and layer is None:
			logger.debug("both path and layer argument was empty. Nothing to do.")
			return self

		origin = self.origin
		newOrigin = origin

		if path is not None:
			newOrigin = newOrigin.withLocalPath(path)
		if layer is not None:
			newOrigin = newOrigin.inLayer(layer)

		logger.debug(f"target:{origin}, new local path:{path}, new layer: {newOrigin.layer.path}")
		logger.debug(f"origin:{origin}, newOrigin:{newOrigin}")

		if origin == newOrigin:
			logger.debug("New location same as previos")
			return

		# Check that the target location is not occupied
		# Which it is if there is a file there, and that
		# files origin is not ours
		if newOrigin.exists() and newOrigin.origin != origin:
			raise FileExistsError(f"Cannot move file {origin} to {newOrigin}. File exists.")

		# Check for out of sync condition
		# We need to make sure that the target origin local path
		# does not exist in a any of the layers.
		for layer in self.layer.siblings:
			if (p := newOrigin.inLayer(layer).origin).exists() and p != origin:
				raise Exceptions.FileConflictError("Filetree out of sync!")

		# Check that the directory structure
		# exists in the target layer (Is not just symlinked)
		linked = newOrigin.getLocalParent().stepTowards(newOrigin)
		assert(linked.isSymlink() or not linked.exists())
		if linked != newOrigin:
			logger.debug("Target origin path was symlinked. Creating directory structure")
			logger.debug(f"- unlink {linked}")
			linked.unlink()
			logger.debug(f"- mkdir {linked}")
			linked.path.mkdir(parents=True, exist_ok=True)


		logger.debug("Removing links to the previous origin file")
		for layer in self.layer.layerSet.layers:
			if origin.inLayer(layer).isSymlink():
				origin.inLayer(layer).unlink()

		# Move the file
		logger.debug("Copying the file to the spesified location.")
		if origin.isDir():
			shutil.copytree(origin.path, newOrigin.path)
		else:
			shutil.copy(origin.path, newOrigin.path)
		
		assert(newOrigin.path.exists())
		# Todo. Confirm checksum of new file
		logger.debug("Everything seems ok.")
		if origin.isDir():
			logger.debug("Deleting the original directory.")
			shutil.rmtree(origin.path)
		else:
			logger.debug("Deleting the original file.")
			origin.unlink(force=True)

		logger.debug("Creating links to the new origin file")
		for layer in self.layer.siblings:
			if layer != newOrigin.layer:
				newOrigin.inLayer(layer).symlinkTo(newOrigin.layer)
		
		logger.debug("Done.")
		return newOrigin

	def listdir(self, files=True, dirs=True, symlinks=True):
		if not self.isDir():
			raise NotADirectoryError("")

		dirList = [
			LayerFile(self.layer, self.path / p) for p in os.listdir(self.path)
		]

		if not files:
			dirList = [p for p in dirList if not p.isFile()]
		
		if not dirs:
			dirList = [p for p in dirList if not p.isDir()]
		
		if not symlinks:
			dirList = [p for p in dirList if not p.isSymlink()]

		return dirList

	def isDir(self):
		return self.absolute.resolve().is_dir()

	def isFile(self):
		return self.absolute.is_file()

	def isSymlink(self):
		return self.absolute.is_symlink()

	def isOrigin(self):
		return self.absolute.resolve() == self.absolute

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

	def relativeTo(self, path: LayerFile):
		return LayerFile(self.layer, self.path.relative_to(path))

	def rmdir(self):
		return self.path.rmdir()

	def exists(self):
		return self.path.exists()

	@property
	def isRoot(self):
		return len(self.path.parts) == 0

	@property
	def parent(self):
		if self.isRoot:
			return None
		return self.withPath(self.path.parent)

	@property
	def layer(self) -> lib.Layer:
		return self._layer

	@property
	def origin(self) -> LayerFile:
		return self.layer.layerSet.origin(self)

	@property
	def path(self) -> Path:
		return self._path

	@property
	def name(self) -> str:
		return self.path.name

	@property
	def absolute(self) -> Path:
		return self.layer.root / self.path

	def __str__(self) -> str:
		return str(self.absolute)

	def __truediv__(self, other:Union[Path, str]):
		return self.withPath(self.path/other)

	def __key(self):
		return (self.absolute)

	def __hash__(self):
		return hash(self.__key)

	def __eq__(self, other):
		if isinstance(other, __class__):
			return self.__key() == other.__key()
		if isinstance(other, Path):
			return self.absolute == other
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, __class__):
			return self.__key() < other.__key()
		return NotImplemented
	
	def __gt__(self, other):
		if isinstance(other, __class__):
			return self.__key() > other.__key()
		return NotImplemented

