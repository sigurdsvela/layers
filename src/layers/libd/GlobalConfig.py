from pathlib import Path

class GlobalConfig:
	def __init__(self, home):
		from layers.lib import GlobalConsts
		
		config_dir = Path(GlobalConsts.GLOBAL_CONFIG_DIR.format(home=home))
		if not config_dir.is_dir():
			config_dir.mkdir()
