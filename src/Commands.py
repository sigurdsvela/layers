from LayerSet import LayerSet
from LayerSetConfig import LayerSetConfig
from pathlib import Path

def mv(args):
	if (LayerSet.isInLayerset(args.setpath)):
		pass


def new(args):
	if (not LayerSet.isInLayerset(args.setpath)):
		LayerSetConfig.create(args.mount)

def sync(args):
	pass