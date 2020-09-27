from argparse import ArgumentParser
from pathlib import Path
from layers.lib import Layer
from layers.lib import LayerSet

import logging

logger = logging.getLogger("layers:sync")

info = {
	'name': 'sync',
	'help': 'Sync files in a layerset, making sure everyfile is symbolically located in every layer'
}

defaults = {}

def setup(_: ArgumentParser):
	pass

def run(target_layer: Path, **kwargs):
	logger.debug("Running sync")

	layerSet = LayerSet.fromLayer(Layer(target_layer))

	print("Syncing layers:")
	for layer in layerSet.layers:
		print(" - " + str(layer.path))
	
	LayerSet.fromLayer(Layer(target_layer)).sync()

	print("Done")
