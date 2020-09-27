from importlib.machinery import SourceFileLoader
from pathlib import Path
from os.path import dirname
import traceback
import argparse
import os
import sys
import logging
from layers.cli import Runner, commands

logLevel = logging.WARNING

root = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
root.setLevel(logLevel)
handler.setLevel(logLevel)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

main = argparse.ArgumentParser(
	prog="layers",
	description=""
)
main.add_argument(
	'--layer', '-l',
	type=Path,
	action="store",
	dest="target_layer",
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
	loadedCommands[module.info['name']].setup(subcommandParser)

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



