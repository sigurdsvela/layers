from argparse import ArgumentParser
from pathlib import Path
from layers.lib import LayerSet, LayerFile, Layer, UserConfig, Level

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
		type=Level.parseFactory(),
		dest="level",
		default=-1,
		help="The level number to assign the new layer. If a layer of this level exists, the new one will be placed on the given level, and levels from there on down will be shifted down."
	)

	level.add_argument(
		"--top", "-t",
		dest="level",
		action="store_const",
		const=Level.TOP,
		help="Add the new layer as the top level."
	)

	level.add_argument(
		"--bottom", "-b",
		dest="level",
		action="store_const",
		const=Level.BOTTOM,
		help="Add the new layer as the top level."
	)

	parser.add_argument(
		"mount",
		type=str,
		help="The mount point of the new layer"
	)

def run(config: UserConfig, target_set: LayerSet, mount: str, level: Level, **kwargs):
	from layers.lib import Layer, UserConfig

	print(f"Creating a new layer for set {target_set.name} at {mount}")
	
	target_set.addLayer(Layer(root=mount, layerSet=target_set), atLevel=level)
