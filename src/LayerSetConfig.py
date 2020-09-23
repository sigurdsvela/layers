import LayerSet
from GlobalConsts import SET_CONFIG_DIR
import yaml
from pathlib import Path

class LayerSetConfig:
	def __init__(self, set: LayerSet):
		self._set = set
		self._layers_config_path = set.root() / SET_CONFIG_DIR
		self._layers_config_file = Path(self._layers_config_file).open('rw')
		self._layers_config = yaml.load_safe(self._layers_config_file.read())

	@property
	def layers():
		pass
