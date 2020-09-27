from argparse import ArgumentParser
from pathlib import Path
from layers.lib import Layer
from layers.lib import LayerSet

info = {
	'name': 'new',
	'help': ''
}

defaults = {
	"level": -1
}

def setup(parser: ArgumentParser):
	level = parser.add_mutually_exclusive_group()
	level.add_argument(
		"-l", "--level",
		type=int,
		dest="level",
		default=-1,
		help="The level number to assign the new layer. If a layer of this level exists, the new one will be placed on the given level, and levels from there on down will be shifted down."
	)

	level.add_argument(
		"--top", "-t",
		dest="level",
		action="store_const",
		const="top",
		help="Add the new layer as the top level."
	)

	level.add_argument(
		"--bottom", "-b",
		dest="level",
		action="store_const",
		const="bottom",
		help="Add the new layer as the top level."
	)

	parser.add_argument(
		"mount",
		type=Path,
		help="The mount point of the new layer"
	)

def run(target_layer: Path, mount: Path, level, **kwargs):
	from layers.lib import Layer
	from layers.lib import LayerConfig

	if not mount.exists():
		mount.mkdir()
	
	if not mount.is_dir():
		raise Exception("Target mount is a file. Must be directory")

	if (not Layer.isInLayer(target_layer)):
		Layer.createSet(mount.resolve().absolute())
	else:
		layer = Layer(target_layer.absolute())
		layer.createLayer(mount.resolve().absolute(), level)
