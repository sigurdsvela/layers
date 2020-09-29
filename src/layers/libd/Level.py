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

	def __init__(self, level: Union[int, RelativeLevel]):
		self.level = level

	def abs(self, currentLevel=0, maxLevel=0):
		if (self.level == RelativeLevel.UP):
			return max(0, min(currentLevel + 1, maxLevel))
		if (self.level == RelativeLevel.DOWN):
			return max(0, min(currentLevel - 1, maxLevel))
		if (self.level == RelativeLevel.TOP):
			return maxLevel
		if (self.level == RelativeLevel.BOTTOM):
			return 0

Level.TOP = Level(RelativeLevel.TOP)
Level.BOTTOM = Level(RelativeLevel.BOTTOM)
Level.DOWN = Level(RelativeLevel.DOWN)
Level.UP = Level(RelativeLevel.UP)

