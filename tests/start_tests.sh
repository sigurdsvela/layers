#!/bin/bash
python3 ./tests/setup.py
python3 -m unittest discover --verbose -s ./tests -p "Test*.py"