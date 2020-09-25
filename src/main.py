import traceback
import argparse
import os
import sys
import Commands
from pathlib import Path
from Exceptions import InvalidLayersPathException

main = argparse.ArgumentParser(
	prog="layers",
	description=""
)
main.add_argument(
	'--layer', '-l',
	type=Path,
	action="store",
	dest="layer_path",
	required=False,
	default=os.getcwd(),
	help='A path to the root of, or a file withing a layer. Designates the target layer to operate on, or the target layer-set.'
)

main.add_argument(
	'--verbose', '-v',
	action="store_const",
	dest="verbose",
	default=False,
	const=True,
	help="Print debug info"
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
	type=Path,
	help="The mount point of the new layer"
)

level = new.add_mutually_exclusive_group()
level.add_argument(
	"-l", "--level",
	type=int,
	dest="level",
	default=-1,
	help="The level number to assign the new layer. If a layer of this level exists, the new one will be placed on the given level, and levels from there on down will be shifted down."
)

level.add_argument(
	"--top", "-t",
	dest="level",
	action="store_const",
	const="top",
	help="Add the new layer as the top level."
)

level.add_argument(
	"--bottom", "-b",
	dest="level",
	action="store_const",
	const="bottom",
	help="Add the new layer as the top level."
)

### Purge ###
purge = subcommands.add_parser(
	'purge',
	help="Remove any broken link from the entire layerset connected to the target layer."
)

### Move ###
move = subcommands.add_parser(
	'mv',
	help="move a file from one layer to another"
)

move_dst_group = move.add_mutually_exclusive_group(required = False)
move_dst_group.add_argument(
	'--up', '-u',
	help="Move one level up",
	dest="level",
	const="up",
	action="store_const"
)

move_dst_group.add_argument(
	'--down', '-d',
	help="Move one level down",
	dest="level",
	const="down",
	action="store_const"
)

move_dst_group.add_argument(
	'--top', '-t',
	help="Move too top level",
	dest="level",
	const="top",
	action="store_const"
)

move_dst_group.add_argument(
	'--bottom', '-b',
	help="Move too bottom level",
	dest="level",
	const="bottom",
	action="store_const"
)

move_dst_group.add_argument(
	'--level', '-l',
	type=int,
	help="Move the file to the level level spesified"
)

move.add_argument(
	'old_name',
	type=Path
)

move.add_argument(
	'new_name',
	type=Path,
	nargs='?'
)

# Sync
sync = subcommands.add_parser(
	'sync',
	help="Sync files in a layerset, making sure everyfile is symbolically located in every layer"
)


rawArgs = sys.argv[1:]
if (len(rawArgs) == 0):
	rawArgs = ['-h']

args = main.parse_args(rawArgs)
command_function = getattr(Commands, args.command)

try:
	command_function(args)
except Exception as err:
	message = "{0}".format(err)
	if message == "":
		message = "Unknown Error"
	
	if args.verbose:
		traceback.print_exc(file=sys.stdout)
	sys.exit(message)


sys.exit(0)



