from importlib.machinery import SourceFileLoader
from pathlib import Path
from os.path import dirname
import traceback
import argparse
import os
import sys
import logging
from layers.cli import Runner, commands
from layers.lib import LayerSet, UserConfig
import copy

main = argparse.ArgumentParser(
	prog="layers",
	description=""
)

main.add_argument(
	'--set', '-s',
	type=LayerSet.parseFactory(UserConfig.forCurrentUser(), Path.cwd()),
	action="store",
	dest="target_set",
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


# Do partial parse to allow the subsequent arguments type
# definition to have more context
temp = copy.deepcopy(main)
temp.add_argument(
	'none',
	dest='none',
	nargs='*'
)
rawArgs = sys.argv[1:]
if (len(rawArgs) == 0):
	rawArgs = ['-h']

args = main.parse_args(rawArgs)
rootArgs = rawArgs


##################
## SUB COMMANDS ##
##################
subcommands = main.add_subparsers(
	dest='command',
	help='Sub commands'
)

loadedCommands: dict = {}

for command in commands.__all__:
	module = SourceFileLoader(
		fullname = str(command),
		path = str(
			(Path(__file__).parent.parent / 'src/layers/clid/commands' / (command + '.py'))
				.resolve()
				.absolute()
		)
	).load_module()

	subcommandParser = subcommands.add_parser(
		module.info['name'],
		help=module.info['help']
	)

	loadedCommands[module.info['name']] = module
	loadedCommands[module.info['name']].setup(
		parser=subcommandParser,
		config=UserConfig.forCurrentUser(),
		cwd=Path.cwd()
		**vars(rootArgs)
	)

rawArgs = sys.argv[1:]
if (len(rawArgs) == 0):
	rawArgs = ['-h']

args = main.parse_args(rawArgs)
commandModule = loadedCommands[args.command]

runner = Runner()

try:
	vargs = vars(args)
	del vargs['command']
	runner.run(command=commandModule, **vargs)
except Exception as err:
	message = "{0}".format(err)
	if message == "":
		message = "Unknown Error"
	
	#if args.verbose:
	traceback.print_exc(file=sys.stdout)
	sys.exit(message)


sys.exit(0)



