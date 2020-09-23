from pathlib import Path
from GlobalConsts import GLOBAL_CONFIG_DIR

class GlobalConfig:
	def __init__(self.home = Path.home()):
		config_dir = Path(GLOBAL_CONFIG_DIR.format(home=home))
		if (not is_dir(config_dir)):
			config_dir.mkdir()