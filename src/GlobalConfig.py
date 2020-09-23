from pathlib import Path
from GlobalConsts import GLOBAL_CONFIG_DIR

class GlobalConfig:
	def __init__(self, home):
		config_dir = Path(GLOBAL_CONFIG_DIR.format(home=home))
		if not config_dir.is_dir(config_dir):
			config_dir.mkdir()
		pass
