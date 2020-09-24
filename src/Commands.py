from Exceptions import FileConflictException
from pathlib import Path
import logging
import os
import Util
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR)
debug = logging.debug

def mv(args):
	from Layer import Layer

	# The layer the file is currently in
	layer = Layer(Layer.findRoot(
		Path(args.old_name).resolve().absolute()
	))

	oldLayerPath = Path(args.old_name).resolve().absolute().relative_to(layer.path)

	if 'new_name' in args and type(args.new_name) == str:
		newLayerPath = Path(args.new_name).absolute().relative_to(layer.path)
	else:
		newLayerPath = oldLayerPath

	# Remove all links to the file from other layers
	# Move the file to the spesified path
	for layerPath in layer.layers:
		if (layerPath / oldLayerPath).is_symlink():
			(layerPath / oldLayerPath).unlink()
		else:
			(layerPath / oldLayerPath).rename(layerPath / newLayerPath)

	level = layer.layers.index(str(layer.path))
	maxLevel = len(layer.layers) - 1

	# Move the file to the spesified level (Pass if none spesified)
	if 'layer' in args:
		layerid = args.layer
		if type(layerid) == int:
			# Move to the spesified layer
			Path(layer.path / newLayerPath).rename(layer.layers[layerid] / newLayerPath)
		elif layerid == 'up':
			Path(layer.path / newLayerPath).rename(layer.layers[max(level - 1, 0)] / newLayerPath)
		elif layerid == 'down':
			Path(layer.path / newLayerPath).rename(layer.layers[min(level + 1, maxLevel)] / newLayerPath)
		elif layerid == 'top':
			Path(layer.path / newLayerPath).rename(layer.layers[0] / newLayerPath)
		elif layerid == 'bottom':
			Path(layer.path / newLayerPath).rename(layer.layers[maxLevel] / newLayerPath)
		else:
			raise Exception(f"Cant move file to layer {layer}")


	# Resync
	layer.sync()


def new(args):
	from Layer import Layer
	from LayerConfig import LayerConfig

	if not args.mount.exists():
		args.mount.mkdir()
	
	if not args.mount.is_dir():
		raise Exception("Path was a file. Must be directory")

	if (not Layer.isInLayer(args.layer_path)):
		debug(f"{str(args.layer_path)} not within an existing layer. Creating new set at {str(args.mount)}")
		Layer.createSet(args.mount.resolve().absolute())
	else:
		debug("New from within a layer. Creating new level.")
		layer = Layer(args.layer_path.absolute())
		debug(f"Root set: {str(args.layer_path)}")
		layer.createLayer(args.mount.resolve().absolute(), args.level)
		debug(f"new level at: {str(args.mount)}")

def sync(args):
	from Layer import Layer
	from LayerConfig import LayerConfig

	Layer(args.layer_path).sync()
