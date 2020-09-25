#!/bin/bash
PYTHONPATH_BAK=$PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 -m unittest discover --verbose -s ./tests -p "Test*.py"
PYTHONPATH=$PYTHONPATH_BAK
