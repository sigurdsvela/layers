import argparse
import os
import sys
import Commands
from Exceptions import InvalidLayersPathException

main = argparse.ArgumentParser(
	prog="layers",
	description=""
)
main.add_argument(
	'--set', '-s',
	nargs = 1,
	type=str,
	dest="setpath",
	default=os.getcwd(),
	help='Path to a file withing or to the root directory of a layer withing the layerset to operate on. Defaults to the closest layer up the file tree from pwd.'
)

##################
## SUB COMMANDS ##
##################
subcommands = main.add_subparsers(
	dest='command',
	help='Sub commands'
)

### New ###
new = subcommands.add_parser(
	'new',
	help="Add a layer to a layerset, or create a new layerset"
)

new.add_argument(
	"mount",
	type=str,
	help="The mount point of the new layer"
)

new.add_argument(
	"level",
	type=int,
	help="The level number to assign the new layer"
)

### Move ###
move = subcommands.add_parser(
	'mv',
	help="move a file from one layer to another"
)

move_dst_group = move.add_mutually_exclusive_group(required = True)
move_dst_group.add_argument(
	'--up', '-u',
	help="Move one layer up",
	dest="layer",
	const="up",
	action="store_const"
)

move_dst_group.add_argument(
	'--down', '-d',
	help="Move one layer down",
	dest="layer",
	const="down",
	action="store_const"
)

move_dst_group.add_argument(
	'--top', '-t',
	help="Move too top layer",
	dest="layer",
	const="top",
	action="store_const"
)

move_dst_group.add_argument(
	'--bottom', '-b',
	help="Move too bottom layer",
	dest="layer",
	const="bottom",
	action="store_const"
)

move_dst_group.add_argument(
	'--out', '-o',
	help="Move out of the layer set, spesifies path",
	type=str,
	dest="layer"
)

move_dst_group.add_argument(
	'--layer', '-l',
	type=int,
	help="Move the file to the layer level spesified"
)

move.add_argument(
	'file_name',
	type=str
)

# Sync
sync = subcommands.add_parser(
	'sync',
	help="Sync files in a layerset, making sure everyfile is symbolically located in every layer"
)


rawArgs = sys.argv[1:]


args = main.parse_args(rawArgs)
command_function = getattr(Commands, args.command)
command_function(args)



