from argparse import ArgumentParser
from pathlib import Path
from layers.lib import LayerSet, LayerFile, Layer, UserConfig, Level

info = {
	'name': 'newset',
	'help': ''
}

defaults = {
	"level": -1
}

def setup(parser: ArgumentParser):
	level = parser.add_mutually_exclusive_group()
	parser.add_argument(
		"name",
		type=str,
		help="The name of the new set"
	)

def run(config: UserConfig, name: str, **kwargs):
	from layers.lib import Layer, UserConfig

	print(f"Creating layer set '{name}'")
	
	config.addLayerSet(name=name)
