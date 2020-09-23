from Exceptions import FileConflictException
from pathlib import Path
import logging
import os
import Util
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
debug = logging.debug

def mv(args):
	from LayerSet import LayerSet

	if (LayerSet.isInLayerset(args.setpath)):
		pass


def new(args):
	from LayerSet import LayerSet
	from LayerSetConfig import LayerSetConfig

	if not args.mount.exists():
		args.mount.mkdir()
	
	if not args.mount.is_dir():
		raise Exception("Path was a file. Must be directory")

	if (not LayerSet.isInLayerset(args.setpath)):
		debug("New from outside a layerset. Creating new setroot.")
		LayerSet.createSet(args.mount.resolve().absolute())
	else:
		debug("New from within a layerset. Creating new level.")
		layerSet = LayerSet(args.setpath.absolute())
		debug(f"Root set: {str(args.setpath)}")
		layerSet.createLayer(args.mount.resolve().absolute(), args.level)
		debug(f"new level at: {str(args.mount)}")

def sync(args):
	from LayerSet import LayerSet
	from LayerSetConfig import LayerSetConfig

	# Find the "baselayer". The layer, that all other layers .layers file point to
	baseLayer = LayerSet(
		LayerSet(args.setpath).config.path.resolve().parent
	)

	# We will first walk though all the other layers, to make sure all files in each of these layers are present in the base layer
	for layer in baseLayer.layers:
		layerPath = Path(layer)
		if layerPath == baseLayer.path:
			continue

		for root, dirs, files in os.walk(layer):
			for name in files:
				Util.link(layerPath, baseLayer.path, name)

			for name in dirs:
				Util.link(layerPath, baseLayer.path, name)


	# Then walk though the base layer, and make sure any file in the base layers is present in all the other layers
	for root, dirs, files in os.walk(baseLayer.path):
		for name in files:
			for layer in baseLayer.layers:
				layerPath = Path(layer)
				if layerPath == baseLayer.path:
					continue
				Util.link(layerPath, baseLayer.path, name)

		for name in dirs:
			for layer in baseLayer.layers:
				layerPath = Path(layer)
				if layerPath == baseLayer.path:
					continue
				Util.link(layerPath, baseLayer.path, name)
