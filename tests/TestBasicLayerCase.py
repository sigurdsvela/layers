import sys
import unittest
import subprocess
import os
from testconst import TEST_DIR, TEST_LEVEL_1, TEST_LEVEL_2, TEST_LEVEL_3
from unittest import TestCase
from BasicLayerCase import BasicLayerCase
from GlobalConsts import SET_CONFIG_FILE
from Layer import Layer

class TestBasicLayerCase(BasicLayerCase):
	def setUp(self):
		super().setUp()
		super().sync()

	def tearDown(self):
		super().tearDown()

	def test_Setup(self):
		self.assertCountEqual(super().verify(), [])
