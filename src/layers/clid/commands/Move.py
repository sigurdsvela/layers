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

def run(target_layer, path, level, new_path=None, **kwargs):
	from layers.lib import LayerSet, Layer, LayerLocalPath
	from layers.cli import argtype

	level = argtype.level(target_layer, path)(level)

	targetPath = LayerLocalPath(path.absolute())
	targetFile = targetPath.original
	newPath = None
	
	print(f"Moving {targetPath.localPath} ", end="")
	if level is not None:
		print(f"from level {targetPath.layer.level} to {level}", end="")

	if level is not None and new_path is not None:
		print(" and ", end="")

	if new_path is not None:
		newPath = LayerLocalPath(new_path.absolute())
		print(f"to {newPath.localPath}", end="")
	print()

	for layer in targetFile.layer.layers:
		if (p := targetFile.inLayer(layer).path).is_symlink():
			p.unlink()

	if newPath is not None:
		targetFile.path.rename(
			(targetFile := targetFile.withLocalPath(newPath.localPath)).path
		)

	if level is not None:
		newPath = targetFile.inLevel(level)
		newLayer = newPath.layer

		# Here, we check if the destination layer actually has a directory for the file
		# 'Layers' will link a directory directly, if it can.
		# However, this means that if we try to move a file that is INSIDE that directory,
		# TO the layer that only has a symlink for that folder, we must first remove that symlink
		# and create the directory.
		symcheck = Path(newLayer.path)
		for part in newPath.localPath.parent.parts:
			if (symcheck := (symcheck/part)).is_symlink():
				symcheck.unlink()
			if not symcheck.exists():
				symcheck.mkdir()
		
		targetFile.path.rename(newPath.path)
		targetFile = newPath

	LayerSet(targetFile.layer).sync()

