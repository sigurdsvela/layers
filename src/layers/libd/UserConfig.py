from __future__ import annotations
import logging
from yaml import safe_load, dump
from pathlib import Path
from typing import Union
import layers.lib as lib
from uuid import UUID


class UserConfig:
	@classmethod
	def forCurrentUser(cls):
		return cls(Path.home())

	def __init__(self, home: Path):
		from layers.lib import GlobalConsts
		self.home = home
		self.configDir = Path(GlobalConsts.USER_CONFIG_DIR.format(home=str(home)))

		if not self.configDir.is_dir():
			self.configDir.mkdir()

		self.layerSetsConfig = self.configDir / "layersets"
	
		if not self.layerSetsConfig.exists():
			self.layerSetsConfig.touch(mode=0o660)
			self.writeConfig({
				'sets':{}
			})

	@property
	def path(self):
		return self.configDir

	def readConfig(self):
		try:
			return safe_load(fh := self.layerSetsConfig.open('r'))
		except OSError as e:
			raise e
		finally:
			fh.close()

	def writeConfig(self, config):
		try:
			(fh := self.layerSetsConfig.open('w')).write(dump(config))
		except OSError as e:
			raise e
		finally:
			fh.close()

	def addLayer(self,
		layer: Union[lib.Layer, Path],
		toSet: Union[lib.LayerSet, str],
		atLevel: lib.Level = None
	) -> lib.Layer:
		from layers.lib import LayerSet, Layer, Level
		config = self.readConfig()

		if isinstance(toSet, str):
			toSet = self.layerSet(withName=toSet)

		if isinstance(layer, Layer):
			layer = layer.root

		if not toSet.name in config['sets']:
			raise FileNotFoundError(f"LayerSet with name '{toSet.name}' exists")

		if (layerSet := self.layerSet(withLayer=layer)):
			raise FileExistsError(f"Layer at '{layer.root}' allready in set '{layerSet.name}'")
		
		if atLevel is None:
			atLevel = Level.BOTTOM(toSet)

		atLevel = atLevel(toSet)

		if atLevel != Level.BOTTOM(toSet):
			config['sets'][toSet.name]['layers'].insert(
				int(atLevel),
				{
					'root': str(layer)
				}
			)
		else:
			config['sets'][toSet.name]['layers'].extend([{
				'root': str(layer)
			}])

		self.writeConfig(config)
		return Layer(layerSet=toSet, root=layer)


	def addLayerSet(
		self,
		name: str
	) -> lib.LayerSet:
		from layers.lib import LayerSet
		config = self.readConfig()
		
		if name in config['sets']:
			raise FileExistsError(f"LayerSet with naem {name} allready exists")

		config['sets'][name] = {'layers':[]}
		self.writeConfig(config)
		return LayerSet(name=name, config=self)

	def layerSet(self,
		withName: str = None,
		withLayer: Union[lib.Layer, Path] = None,
	) -> lib.LayerSet:
		from layers.lib import LayerSet, Layer
		if withName is not None:
			if withName in self.readConfig()['sets']:
				return LayerSet(name=withName, config=self)
			else:
				return None
		
		assert(isinstance(withLayer, lib.Layer) or isinstance(withLayer, Path))
		if withLayer is not None:
			if (layer := self.layer(withRoot=withLayer.root if isinstance(withLayer, Layer) else withLayer)) is not None:
				return layer.layerSet
		
		return None
	
	@property
	def layerSets(self) -> [lib.LayerSet]:
		from layers.lib import LayerSet
		return [LayerSet(name, self) for name, layers in self.readConfig()['sets'].items()]

	def layers(self, inSet: lib.LayerSet) -> [lib.Layer]:
		from layers.lib import Layer
		logging.getLogger().setLevel(logging.DEBUG)
		logging.getLogger().debug(self.readConfig())
		return [
			Layer(layerSet=inSet, root=Path(layer['root'])) for layer in self.readConfig()['sets'][inSet.name]['layers']
		]

	def layer(self,
		withRoot: Path
	) -> lib.Layer:
		for layerSet in self.layerSets:
			for layer in layerSet.layers:
				if layer.root == withRoot:
					return layer
		return None

	def __key(self):
		return self.home

	def __hash__(self):
		return hash(self.__key)

	def __eq__(self, other):
		if isinstance(other, __class__):
			return self.__key() == other.__key()
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, __class__):
			return self.__key() < other.__key()
		return NotImplemented
	
	def __gt__(self, other):
		if isinstance(other, __class__):
			return self.__key() > other.__key()
		return NotImplemented
