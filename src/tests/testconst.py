# Set by the make file before running the tests
from pathlib import Path

TEST_LEVEL_1 = 'level1'
TEST_LEVEL_2 = 'level2'
TEST_LEVEL_3 = 'level3'

L1 = TEST_LEVEL_1
L2 = TEST_LEVEL_2
L3 = TEST_LEVEL_3

TEST_LEVEL_1_FILE = 'level1_file'
TEST_LEVEL_2_FILE = 'level2_file'
TEST_LEVEL_3_FILE = 'level3_file'

L1_FILE = TEST_LEVEL_1_FILE
L2_FILE = TEST_LEVEL_2_FILE
L3_FILE = TEST_LEVEL_3_FILE

# Overwritten at setup
TEST_DIR = Path("./tests/testdir").resolve().absolute()