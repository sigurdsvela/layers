import LayerSet
from GlobalConsts import SET_CONFIG_FILE
import yaml
from pathlib import Path

class LayerSetConfig:

	@classmethod
	def create(cls, path: Path):
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
		self._config = yaml.safe_load_all(path.open('rw').read())

	@property
	def layers(self):
		pass
