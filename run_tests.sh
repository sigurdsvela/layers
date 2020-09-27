#!/bin/bash

echo "PYTHONPATH=\"$(pwd)/src\" python3 -m unittest discover --verbose -s \"./src/tests\" -p \"Test*.py\""

if [ -z ${1+x} ]; then
	echo "Running all tests"
	PYTHONPATH="$(pwd)/src" python3 -m unittest discover --verbose -s "./src/tests" -p "Test*.py"
else
	echo "Running tests {$@}"
	PYTHONPATH="$(pwd)/src" python3 -m unittest discover --verbose -s "./src/tests" -p "$@"
fi

