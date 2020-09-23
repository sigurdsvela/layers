import os
from GlobalConsts import SET_CONFIG_FILE
from pathlib import Path
from Exceptions import InvalidLayersPathException
import LayerSetConfig

class LayerSet:
	# Starting at some path, walks up the file tree looking
	# for the first instance of a `.layers` configuration directory
	@classmethod
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
			if ((root_path / SET_CONFIG_FILE).exists()):
				break

			# If we are at root, but have not found the config dir
			if len(root_path.parts) == 1:
				raise InvalidLayersPathException()

			root_path = root_path.parent
		return cls(root_path)


	@classmethod
	def isInLayerset(cls, path):
		try:
			cls.find(path)
		except:
			return False
		return True

	def __init__(self, path):
		self._path = path
		self._config = LayerSetConfig.LayerSetConfig(self._path)

	@property		
	def layers(self):
		pass

	@property
	def root(self):
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