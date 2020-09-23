import os
from GlobalConsts import SET_CONFIG_DIR
from pathlib import Path
from Exceptions import InvalidLayersPathException
import LayerSetConfig

class LayerSet:
	# Starting at some path, walks up the file tree looking
	# for the first instance of a `.layers` configuration directory
	@staticmethod
	def find(cls, path: Path):
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
			if ((root_path / SET_CONFIG_DIR).is_dir()):
				break

			# If we are at root, but have not found the config dir
			if len(root_path.parts) == 1:
				raise InvalidLayersPathException()

			root_path = root_path.parent
		return cls(root_path)


	def __init__(self, path):
		self._path = path
		self._config = LayerSetConfig.LayerSetConfig(self._path)

	@property		
	def layers():
		pass

	@property
	def root():
		return self._path

	def addLayer(mount_path):
		pass

	# List files
	# @path the path local to the root of the layer
	def ls(path):
		pass

	# Get the lever where a file is
	def getLayer(path):
		pass