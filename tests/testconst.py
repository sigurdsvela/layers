# Set by the make file before running the tests
from pathlib import Path

TEST_LEVEL_1 = 'level1'
TEST_LEVEL_2 = 'level2'
TEST_LEVEL_3 = 'level3'

TEST_LEVEL_1_FILE = 'level1_file'
TEST_LEVEL_2_FILE = 'level2_file'
TEST_LEVEL_3_FILE = 'level3_file'

# Overwritten at setup
TEST_DIR = Path("./tests/testdir").resolve().absolute()