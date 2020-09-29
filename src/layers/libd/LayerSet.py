from __future__ import annotations
from uuid import UUID
from pathlib import Path
from layers.lib import Layer, Exceptions, UserConfig
import layers.lib as lib
import logging
import copy

# Represents a set of layers in a layer set
class LayerSet:
	@classmethod
	def parseFactory(cls, config: UserConfig, cwd: Path):
		return lambda arg: cls.parse(config, cwd, arg)
	
	@classmethod
	def parse(cls, config:UserConfig, cwd:Path, arg:str):
		if arg:
			layerSet = config.layerSet(withName=arg)
			if layerSet is not None:
				return layerSet
			
			return Exceptions.InvalidArgumentError(
				argType="LayerSet",
				argValue=arg
			)
		else:
			layer = config.layer(withPath=cwd)
			if layer is not None:
				layerSet = layer.layerSet

			if layerSet is not None:
				return LayerSet

			return None


	def __init__(self, name:str = None, config: UserConfig = None):
		self._name  = name
		self._config = config

	def exists(self) -> bool:
		if (self._name is None):
			return False
		if (self._config is None):
			return False
		return (self.config.layerSet(withName=self.name)) is not None

	
	def findLayerFile(self, path: Path):
		from layers.lib import LayerFile
		path = path.absolute()
		layerPath = None
		layer = None
		for l in self.layers:
			try:
				layerPath = path.relative_to(l.root)
				layer = l
				break
			except:
				pass
		if layer is None:
			return None

		return LayerFile(layer, layerPath)

	@property
	def name(self) -> name:
		return self._name

	@property
	def config(self) -> UserConfig:
		return copy.deepcopy(self._config)

	@property
	def layers(self) -> [Layer]:
		return self._config.layers(inSet=self)

	@property
	def files(self):
		# All the files in this layerset
		files = []
		for layer in self.layers:
			files.extend(layer.files)
		return files

	@property
	def dirs(self):
		dirs = []
		for layer in self.layers:
			dirs.extend(layer.dirs)
		return dirs

	def addLayer(self, layer: Layer, atLevel: 'lib.Level'):
		self._config.addLayer(layer, toSet=self, atLevel=atLevel)

	def origin(self, file:'lib.LayerFile') -> 'lib.LayerFile':
		for layer in self.layers:
			f = file.inLayer(layer)
			if f.absolute.resolve() == f.absolute:
				return f
		return None

	def move(self,
		file:'lib.LayerFile',
		toLayer:'lib.Layer'=None,
		toLevel: 'lib.Level'= None
	) -> 'lib.LayerFile':
		pass

	def links(self, toFiles = False, toDirs = False):
		links = []
		for layer in self.layers:
			links.extend(layer.links(toFiles=toFiles, toDirs=toDirs))
		return links

	# Sync the entire layer set
	def sync(self):
		logger = logging.getLogger(".".join([__name__, __file__, str(__class__), "sync"]))
		
		logger.debug(f"Syncing {len(self.files)} files in {len(self.layers)} layers")
		files = self.files
		for f in files:
			logger.debug(f"- {f.absolute} from {f.layer.root}")
			for layer in self.layers:
				if layer == f.layer:
					continue
				
				logger.debug(f"- to {layer.root}")
				if f.inLayer(layer).absolute.exists():
					if f.inLayer(layer).absolute.resolve().samefile(f.absolute.resolve()):
						# Allready linked, we good
						continue
					else:
						raise Exceptions.FileConflictError(f"Conflicting content between layer {layer.level}@{layer.root} and {f.layer.level}@{f.layer.root} for file {f.absolute}")
				else:
					# If the destination does not contain the parent
					# diretory this file is in, then we symlink the entire directory.
					p = f
					while not p.inLayer(layer).absolute.parent.exists():
						p = p.parent
					p.inLayer(layer).absolute.symlink_to(p.absolute)
		
		# Finally, we will check the directory structure of
		# Each of the layers, looking for any directory with ONLY
		# symlinks.
		# Any such directory can then simply be a symlink in itself
		# directory to that directory in another layer
		for layer in self.layers:
			derivdirs = layer.findPurelyDerivativeDirs()
			for ddir in derivdirs:
				ddirls = ddir.listdir()
				origin = ddirls[0].origin.parent

				for link in ddir.listdir():
					assert(link.isSymlink())
					link.unlink()

				ddir.rmdir()
				ddir.symlinkTo(layer=origin.layer)


	# Purge the entire layer set
	def purge(self):
		for layer in self.layers:
			layer.purge()


	def __eq__(self, other):
		if not isinstance(other, LayerSet):
			return False
		
		return (self.name) == (other.name) and (self.layers == other.layers)
