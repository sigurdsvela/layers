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
	targetOrigin = targetPath.origin
	newOrigin = targetOrigin
	
	print(f"Moving {targetPath.localPath} ", end="")
	if level is not None:
		print(f"from level {targetPath.layer.level} to {level}", end="")
		newOrigin = newOrigin.inLevel(level)

	if level is not None and new_path is not None:
		print(" and ", end="")

	if new_path is not None:
		newOrigin = newOrigin.withLocalPath(new_path.absolute().relative_to(targetOrigin.layer.path))
		print(f"to {newOrigin.localPath}", end="")
	

	print()

	targetOrigin.move(newOrigin)
	LayerSet(newOrigin.layer).sync()

