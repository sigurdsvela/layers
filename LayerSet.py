import os
from GlobalConsts import SET_CONFIG_DIR
from pathlib import Path
from Exceptions import InvalidLayersPathException

class LayerSet:

	def __init__(self, path):
		root_path = Path(os.getcwd())
		while True:
			if (os.path.isdir(root_path / SET_CONFIG_DIR)):
				break

			# If we are at root, but have not found the config dir
			if len(root_path.parts) == 1:
				raise InvalidLayersPathException()

			root_path = root_path.parent

		self.path = root_path
				
