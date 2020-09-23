from pathlib import Path
import logging
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
	pass