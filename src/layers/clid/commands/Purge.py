from argparse import ArgumentParser
from pathlib import Path
from layers.lib import Layer
from layers.lib import LayerSet

info = {
	'name': 'purge',
	'help': 'help purge'
}

defaults = {}

def setup(__: ArgumentParser, **_):
	pass

def run(target_set: Layer, **_):
	target_set.purge()
