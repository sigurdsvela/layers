from __future__ import annotations
import logging
from yaml import safe_load, dump
from pathlib import Path
from typing import Union
from layers.lib import GlobalConsts
import layers.lib as lib
from uuid import UUID


class UserConfig:
	@classmethod
	def forCurrentUser(cls):
		return cls(Path.home())

	def __init__(self, home: Path):
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
		layer: lib.Layer,
		toSet: Union[lib.LayerSet, str],
		atLevel: lib.Level = lib.Level.BOTTOM
	) -> lib.Layer:
		from layers.lib import LayerSet, Layer
		config = self.readConfig()

		if isinstance(toSet, LayerSet):
			toSet = toSet.name

		if not toSet in config['sets']:
			raise FileNotFoundError(f"LayerSet with name {toSet} not found exists")

		if (layerSet := self.layerSet(withLayer=layer)):
			raise FileExistsError(f"Layer at '{layer.root}' allready in set '{layerSet.name}'")
		
		targetSet = config['sets'][toSet]
		maxLevel = len(targetSet['layers']) - 1
		config['sets'][toSet]['layers'].insert(
			atLevel.abs(maxLevel=maxLevel),
			{
				'root': str(layer.root)
			}
		)

		self.writeConfig(config)
		return Layer(layerSet=LayerSet(name=toSet, config=self), root=layer.root)


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
		if withName is not None:
			if withName in self.readConfig()['sets']:
				return self.readConfig()['sets'][withName]
			else:
				return None
		
		assert(isinstance(withLayer, lib.Layer) or isinstance(withLayer, Path))
		if withLayer is not None:
			for layerSet in self.layerSets:
				for layer in self.layers(inSet=layerSet):
					if isinstance(withLayer, lib.Layer):
						if layer == withLayer:
							return layer
					else:
						if layer.root == withLayer:
							return layer
		
		return None
	
	@property
	def layerSets(self) -> [lib.LayerSet]:
		from layers.lib import LayerSet
		return [LayerSet(name, self) for name in self.readConfig()['sets']]

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
