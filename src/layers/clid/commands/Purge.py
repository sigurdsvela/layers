from argparse import ArgumentParser
from pathlib import Path
from layers.lib import Layer
from layers.lib import LayerSet

info = {
	'name': 'purge',
	'help': 'help purge'
}

def setup(_: ArgumentParser):
	pass

def run(target_layer: Path, **kwargs):
	LayerSet.fromLayer(Layer(target_layer)).purge()
