#!/bin/bash
TEST_DIR="$(pwd)/testenv"
echo "TEST_DIR=Path(\"$TEST_DIR\").resolve().absolute()" >> ./tests/testdir.py
mkdir -p $TEST_DIR
python3 -m unittest discover --verbose -s ./tests -p "Test*.py"