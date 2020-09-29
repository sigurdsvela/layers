#!/bin/bash


#PYTHONPATH="$(pwd)/src" python3 -m unittest discover --verbose -s "./src/tests/testlib" -p "Test*.py" && \
PYTHONPATH="$(pwd)/src" python3 -m unittest discover --verbose -s "./src/tests/lib" -p "*Test*.py" #&& \
#PYTHONPATH="$(pwd)/src" python3 -m unittest discover --verbose -s "./src/tests/commands" -p "Test*.py"  && \
#PYTHONPATH="$(pwd)/src" python3 -m unittest discover --verbose -s "./src/tests/cli" -p "Test*.py" && \
#PYTHONPATH="$(pwd)/src" python3 -m unittest discover --verbose -s "./src/tests/integration" -p "Test*.py"

