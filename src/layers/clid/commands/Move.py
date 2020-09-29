from argparse import ArgumentParser
from layers.lib import LayerFile, Layer, Level, LayerSet, process, UserConfig
from pathlib import Path

info = {
	"name": "mv",
	"help": "Rename files, or move from a layer to another"
}

defaults = {
	"level": None,
	"new_path": None
}

def setup(
	parser: ArgumentParser,
	target_set: LayerSet,
	config: UserConfig,
	cwd: Path
):
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
		'fromFile',
		type=LayerFile.parserFactory(layerSet=target_set)
	)

	parser.add_argument(
		'toFile',
		type=LayerFile.parserFactory(layerSet=target_set),
		nargs='?'
	)

def run(target_set: Layer, fromFile: LayerFile, level: Level, toFile=LayerFile, **kwargs):
	
	fromFile = fromFile.origin

	if toFile is None:
		toFile = fromFile

	print(f"Moving {fromFile.path} ", end="")
	if level is not None:
		toFile = toFile.inLevel(level)
		print(f"from level {fromFile.layer.level} to {level}", end="")

	if level is not None and toFile is not None:
		print(" and ", end="")

	if toFile is not None:
		print(f"to {toFile.path}", end="")
	print()
	
	process.LayerFileMoveProcess(fromFile=fromFile, toFile=toFile).start().wait()
	target_set.sync()

