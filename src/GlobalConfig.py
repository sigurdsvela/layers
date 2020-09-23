from pathlib import Path
import GlobalConsts



class GlobalConfig:
	def __init__(self, home):
		config_dir = Path(GlobalConsts.GLOBAL_CONFIG_DIR.format(home=home))
		if not config_dir.is_dir():
			config_dir.mkdir()
		pass
