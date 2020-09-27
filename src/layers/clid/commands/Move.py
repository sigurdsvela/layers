import os
from typing import TypeVar, Generic
from argparse import ArgumentParser
from pathlib import Path
from layers.lib import LayerLocalPath, Layer

LevelType = TypeVar('LevelType', int, str)

info = {
	"name": "mv",
	"help": "Rename files, or move from a layer to another"
}

defaults = {
	"level": None,
	"new_path": None
}

def setup(parser: ArgumentParser):
	from layers.cli import argtype
	
	move_dst_group = parser.add_mutually_exclusive_group(required = False)
	move_dst_group.add_argument(
		'--up', '-u',
		help="Move one level up",
		dest="level",
		const="up",
		action="store_const"
	)

	move_dst_group.add_argument(
		'--down', '-d',
		help="Move one level down",
		dest="level",
		const="down",
		action="store_const"
	)

	move_dst_group.add_argument(
		'--top', '-t',
		help="Move too top level",
		dest="level",
		const="top",
		action="store_const"
	)

	move_dst_group.add_argument(
		'--bottom', '-b',
		help="Move too bottom level",
		dest="level",
		const="bottom",
		action="store_const"
	)

	move_dst_group.add_argument(
		'--level', '-l',
		type=int,
		help="Move the file to the level level spesified"
	)

	parser.add_argument(
		'path',
		type=Path
	)

	parser.add_argument(
		'new_path',
		type=Path,
		nargs='?'
	)

def run(path, level, new_path=None, **kwargs):
	from layers.lib import LayerSet
	import logging

	logger = logging.getLogger('layers-mv')
	
	logger.debug("Running 'move' with args:")
	logger.debug(f"path={path}, newpath={new_path}, level={level}")

	targetFile = LayerLocalPath(path.absolute())

	# The layer the file is currently in
	currentLayer = Layer(Layer.findRoot(
		targetFile.path.resolve().absolute()
	))

	logger.debug(f"Original file in level in {currentLayer.level}=({str(currentLayer.path)})/{targetFile.localPath}")

	# Remove all links to the file from other layers
	for layer in currentLayer.layers:
		if targetFile.inLayer(layer).path.is_symlink():
			targetFile.inLayer(layer).path.unlink()
	

	newLocalPath = targetFile

	if new_path is not None:
		newLocalPath = newLocalPath.withLocalPath(LayerLocalPath(new_path.absolute()).localPath)

	# Rename the original
	if newLocalPath.path != targetFile.path:
		logger.debug(f"Renaming file: {str(targetFile.path)} -> {str(newLocalPath.path)}")
		(targetFile.path).rename(newLocalPath.path)

	currentLevel = currentLayer.level
	maxLevel = len(currentLayer.layers) - 1
	newLevel = currentLevel

	# Move the file to the spesified level (Pass if none spesified)
	if level is not None:
		# Move to the spesified layer
		if type(level) == int:
			newLevel = max(min(level, 0), maxLevel)
		elif level == 'up':
			newLevel = max(currentLevel - 1, 0)
		elif level == 'down':
			newLevel = min(currentLevel + 1, maxLevel)
		elif level == 'top':
			newLevel = 0
		elif level == 'bottom':
			newLevel = maxLevel
		else:
			raise Exception(f"Cant move file to layer-level {level}")

		logger.debug(f"Moving file. New layer level {newLevel}, at path {newLocalPath.inLevel(newLevel).layer.path}")
		newLocalPath.path.rename(newLocalPath.inLevel(newLevel).path)

	# Resync
	logger.debug("Syncing layers")
	LayerSet.fromLayer(currentLayer).sync()
