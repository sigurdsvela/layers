import LayerSet
from GlobalConsts import SET_CONFIG_FILE
import yaml
from pathlib import Path
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
debug = logging.debug

class LayerSetConfig:

	@classmethod
	def create(cls, path: Path):
		if path.exists() and not path.is_dir():
			raise Exception("Path exists, but is not a directory")
		
		if (path / SET_CONFIG_FILE).exists():
			raise Exception("This directory is allready a registered layer")

		path = path / SET_CONFIG_FILE
		path.touch(mode=0o660)
		path.open('w').write(yaml.dump({
			'layers': [
				{
					'root': str(path.absolute())
				}
			]
		}))

	def __init__(self, path: Path):
		self._path = path / SET_CONFIG_FILE
		if not (self._path.is_file()):
			raise Exception(f"Tried to create Config instance for path {path}, but could not find config file {self._path}")

		if 'layers' not in self.config:
			raise Exception(f"Corrupt config for path {path}: {self.config}")

	
	def linkTo(self, path):
		(path / SET_CONFIG_FILE).symlink_to(self._path)

	@property
	def layers(self):
		pass

	@property
	def config(self):
		return next(yaml.safe_load_all(self._path.open('r').read()))

	@config.setter
	def config(self, newconfig):
		debug("Writing to config")
		debug(newconfig)
		return self._path.open('w').write(yaml.dump(newconfig))

	def path(self):
		return self._path

	def addLayer(self, mount: Path, level: int = -1):
		debug(f"Adding new layer to layerset with path {self._path}")
		debug("Current config")
		debug(self.config)
		debug("Layers")
		debug(self.config["layers"])
		tmpConfig = self.config
		if (level == -1):
			debug("- Appending layer to end")
			tmpConfig["layers"].append({ 'root': str(mount.absolute()) })
		else:
			debug(f"- Insering layer at {level}")
			tmpConfig["layers"].insert({ 'root': str(mount.absolute()) }, level)
		self.config = tmpConfig

	def _flush(self):
		self._path.open('w').write(yaml.dump(self.config))


__all__ = 'LayerSetConfig'