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

	if 'new_name' in args and not args.new_name is None:
		newLayerPath = Path(args.new_name).absolute().relative_to(
			Layer.findRoot(
				Path(args.new_name).absolute()
			)
		)
	else:
		newLayerPath = oldLayerPath

	# Remove all links to the file from other layers
	for layerPath in layer.layers:
		if (layerPath / oldLayerPath).is_symlink():
			(layerPath / oldLayerPath).unlink()

	# Rename the original
	if not newLayerPath is None:
		(layer.path / oldLayerPath).rename(layer.path / newLayerPath)

	

	currentLevel = layer.layers.index(str(layer.path))
	maxLevel = len(layer.layers) - 1

	# Move the file to the spesified level (Pass if none spesified)
	if 'level' in args and args.level != None:
		newLevel = args.level
		if type(newLevel) == int:
			# Move to the spesified layer
			Path(layer.path / newLayerPath).rename(layer.layers[newLevel] / newLayerPath)
		elif newLevel == 'up':
			Path(layer.path / newLayerPath).rename(layer.layers[max(currentLevel - 1, 0)] / newLayerPath)
		elif newLevel == 'down':
			Path(layer.path / newLayerPath).rename(layer.layers[min(currentLevel + 1, maxLevel)] / newLayerPath)
		elif newLevel == 'top':
			Path(layer.path / newLayerPath).rename(layer.layers[0] / newLayerPath)
		elif newLevel == 'bottom':
			Path(layer.path / newLayerPath).rename(layer.layers[maxLevel] / newLayerPath)
		else:
			raise Exception(f"Cant move file to layer-level {newLevel}")


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



def purge(args):
	from LayerSet import LayerSet
	from Layer import Layer

	LayerSet.fromLayer(Layer(args.layer_path)).purge()

