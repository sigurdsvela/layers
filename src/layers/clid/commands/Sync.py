from argparse import ArgumentParser
from pathlib import Path
from layers.lib import Layer,LayerSet

import logging

logger = logging.getLogger("layers:sync")

info = {
	'name': 'sync',
	'help': 'Sync files in a layerset, making sure everyfile is symbolically located in every layer'
}

defaults = {}

def setup(_: ArgumentParser):
	pass

def run(target_set: LayerSet, **kwargs):
	logger.debug("Running sync")

	print("Syncing layers:")
	for layer in target_set.layers:
		print(" - " + str(layer.root))
	
	target_set.sync()

	print("Done")
