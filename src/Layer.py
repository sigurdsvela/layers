import os
from GlobalConsts import SET_CONFIG_FILE
from pathlib import Path
from Exceptions import InvalidLayersPathException
from LayerConfig import LayerConfig
import Util

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
			if ((root_path / SET_CONFIG_FILE).exists()):
				break

			# If we are at root, but have not found the config dir
			if len(root_path.parts) == 1:
				raise InvalidLayersPathException()

			root_path = root_path.parent
		return root_path


	@classmethod
	def isInLayer(cls, path):
		try:
			cls.findRoot(path)
		except InvalidLayersPathException:
			return False
		return True
	

	@classmethod
	def createSet(cls, layer: Path):
		if not layer.exists():
			layer.mkdir()
		if not layer.is_dir():
			raise Exception("Tried to create set on file.")
		LayerConfig.create(layer)


	def __init__(self, path):
		if not path.exists():
			raise FileNotFoundError("Cant create Layer object for a non existent file. Use .crateSet or .createLayer")
		if not path.is_dir():
			raise NotADirectoryError("Cant create Layer object for a path to a file. Must be a directory.")

		self._path = path
		self._config = LayerConfig(self._path)


	def createLayer(self, layer: Path, level: int = -1):
		if not layer.exists():
			layer.mkdir()
		if not layer.is_dir():
			raise Exception('Can not create layer. Path exist, but is not a directory')
		
		self._config.linkTo(layer)
		self._config.addLayer(layer, level)

	@property
	def config(self):
		return self._config

	@property		
	def layers(self):
		return self.config.layers

	@property
	def path(self):
		return self._path

	def addLayer(self, mount_path):
		pass

	# List files
	# @path the path local to the root of the layer
	def ls(self, path):
		pass

	# Get the lever where a file is
	def getLayer(self, path):
		pass


	# Remove all broken links from this layer
	def purge(self):
		for root, dirs, files in os.walk(self.path):
			paths = files
			paths.extend(dirs)
			paths = [LayerLocalPath(self.path, (root / Path(p)).relative_to(self.path)) for p in paths]
			for fpath in paths:
				if fpath.fullPath.is_symlink():
					if not fpath.fullPath.resolve(strict=False).exists():
						fpath.fullPath.unlink()

	def sync(self):
		# Find the "baselayer". The layer, that all other layers .layers file point to
		baseLayer = Layer(
			self.config.path.resolve().parent
		)

		# All layers to base layer
		# The base layer to all layers
		iteration = [(layer, baseLayer.path) for layer in baseLayer.layers]
		iteration.extend([(baseLayer.path, layer) for layer in baseLayer.layers])

		for llayer, rlayer in iteration:
			llayerPath = Path(llayer)
			rlayerPath = Path(rlayer)

			if llayerPath == rlayerPath:
				continue

			for root, dirs, files in os.walk(llayerPath):
				fpaths = dirs
				fpaths.extend(files)
				fpaths = [(root / Path(p)).relative_to(llayerPath) for p in fpaths]
				for fpath in fpaths:
					# Check that the original exists
					if (llayerPath/fpath).is_symlink():
						orig = (llayerPath/fpath).resolve(strict = False).absolute()
						if not orig.exists():
							raise FileNotFoundError(f"Sync Failed: Original for '{fpath}' is missing.")
					
					# Make sure it is linked
					Util.link(llayerPath, rlayerPath, fpath)

__all__ = 'Layer'