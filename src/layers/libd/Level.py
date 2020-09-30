from __future__ import annotations
from pathlib import Path
from typing import Union
from enum import Enum
import layers.lib as lib

class RelativeLevel(Enum):
	TOP = 'top'
	BOTTOM = 'bottom'
	DOWN = 'down'
	UP = 'up'

class Level:
	@classmethod
	def parseFactory(cls, **_):
		return cls.parse

	@classmethod
	def parse(cls, arg:str, **_):
		from layers.lib import Exceptions
		level = None
		try:
			level = Level(int(arg))
		except ValueError:
			try:
				level = Level(RelativeLevel(arg))
			except ValueError:
				return Exceptions.InvalidArgumentError(argValue=arg, argType='Level')
		
		if level is not None:
			return Level(level)

	def __init__(self, level: Union[int, lib.Level, RelativeLevel], offset = None):
		if isinstance(level, __class__):
			self.level = level.level
			self._targetSet = level._targetSet
			self._targetLayer = level._targetLayer
			self.offset = offset if offset is not None else level.offset
		elif isinstance(level, int) or isinstance(level, RelativeLevel):
			self.level = level
			self._targetSet = None
			self._targetLayer = None
			self.offset = offset if offset is not None else 0
		else:
			raise NotImplementedError

	def __call__(self, target):
		from layers.lib import Layer, LayerSet

		if isinstance(target, Layer):
			self._targetSet = None
			self._targetLayer = target
		elif isinstance(target, LayerSet):
			self._targetSet = target
			self._targetLayer = None
		else:
			return NotImplemented
		return self


	def abs(self):
		maxLevel = 0xFFFFFFFF
		currentLevel = 0
		
		if self._targetSet is not None:
			maxLevel = len(self._targetSet.layers)-1

		if self._targetLayer is not None:
			maxLevel = len(self._targetLayer.siblings)-1
			currentLevel = self._targetLayer.level

		maxLevel = max(0, maxLevel)

		absLevel = None
		if self._targetLayer is not None:
			if (self.level == RelativeLevel.UP):
				absLevel = max(0, min(currentLevel - 1, maxLevel))
			if (self.level == RelativeLevel.DOWN):
				absLevel = max(0, min(currentLevel + 1, maxLevel))
		elif self.level == RelativeLevel.UP or self.level == RelativeLevel.DOWN:
			absLevel = 0

		if (self.level == RelativeLevel.TOP):
			absLevel = 0
		if (self.level == RelativeLevel.BOTTOM):
			absLevel = maxLevel
		
		if absLevel is None:
			absLevel = self.level
		
		assert isinstance(absLevel, int), f"Unexpected type {type(self.level)}"

		return absLevel + self.offset

	def __index__(self):
		return self.abs()

	def __sub__(self, other):
		if not isinstance(other, int):
			return NotImplemented
		return Level(level=self, offset=self.offset-other)

	def __add__(self, other):
		if not isinstance(other, int):
			return NotImplemented
		return Level(level=self, offset=self.offset+other)

Level.TOP = Level(RelativeLevel.TOP)
Level.BOTTOM = Level(RelativeLevel.BOTTOM)
Level.DOWN = Level(RelativeLevel.DOWN)
Level.UP = Level(RelativeLevel.UP)

