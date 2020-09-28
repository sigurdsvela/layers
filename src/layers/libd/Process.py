import sys
from pathlib import Path
from threading import Thread
from datetime import timedelta, datetime
from layers.lib import LayerLocalPath
import shutil
import logging

logger = logging.getLogger(".".join([__name__, __file__]))

class Process:
	def __init__(self, **kwargs):
		self.function = kwargs['function']
		self.kwargs = kwargs['kwargs']
		self.name =  kwargs['name'] if 'name' in kwargs else None
		self.stdout = kwargs['stdout'] if 'stdout' in kwargs else sys.stdout
		self.processThread = Thread(target=self._threadRunner, args=(self,), name=self.name)
		self._handleStatus = kwargs['handleStatus'] if 'handleStatus' in kwargs else self.handleStatus

	def start(self, onComplete: callable = None):
		self.onComplete = onComplete
		self.startTime = datetime.now()
		self.processThread.start()
		return self

	def handleStatus(self):
		pass

	def statusProcessor(self, **kwargs):
		args = {
			**{
				'currentJob' : None,
				'eta': None, # datetime
				'progress': None
			},
			**kwargs,
			**{
				'startTime': self.startTime
			}
		}
		
		self.stdout.write(self._handleStatus(**args, stdio=self.stdout))
		self.stdout.flush()
		

	def wait(self):
		self.processThread.join()

	def _threadRunner(self, *args, **kwargs):
		self.function(**self.kwargs, onStatus=self.statusProcessor)
		self.stdout.write("\n")
		
		if self.onComplete is not None:
			self.onComplete()


class LayerFileMoveProcess(Process):

	def __init__(self, fromFile:LayerLocalPath, toFile:LayerLocalPath, stdout = sys.stdout):
		super().__init__(
			function=self._move,
			kwargs={
				'fromFile': fromFile,
				'toFile': toFile
			},
			name = ''
		)

	def _move(self, fromFile:LayerLocalPath, toFile:LayerLocalPath, onStatus):
		from time import sleep
		import os
		
		def getSize(path:Path):
			if path.is_file() or path.is_symlink():
				stat = os.stat(path)
				return stat.st_blksize * stat.st_blocks
			elif path.is_dir():
				total = 0
				files = [Path(p) for p in os.listdir(path)]
				for f in files:
					total += getSize(path/f)
				return total
			else:
				return 0

		fromFileSize = getSize(fromFile.path)
		runStatus = True

		def copyStatusThread():
			minSleepMs=30
			while runStatus:
				timeToCalc = timedelta(seconds=0)
				startCalc = datetime.now()
				try:
					currentSize = getSize(toFile.path)
				except OSError:
					continue
				timeToCalc = datetime.now() - startCalc
				if fromFileSize != 0:
					onStatus(currentSize=currentSize, progress=(float(currentSize)/float(fromFileSize)))
				else:
					onStatus(currentSize=currentSize, progress=1)
				sleep(max(timedelta(milliseconds=minSleepMs), timeToCalc*3).total_seconds())
		
		copyStatusThread = Thread(target=copyStatusThread)
		copyStatusThread.start()

		fromFile.move(toFile, onTempContainerCreate=lambda path : path)
		runStatus = False

	def handleStatus(self, currentJob, currentSize, eta, progress, startTime, **kwargs):
		bar_len = 60
		filled_len = int(round(bar_len * progress))

		percents = round(100.0 * progress, 1)
		bar = '=' * filled_len + '-' * (bar_len - filled_len)

		currentSize /= 8 # To bytes

		i = 0
		currentSize = float(currentSize)
		while currentSize > 999:
			currentSize /= 1024.0
			i += 1

		pref = ['', 'Ki', 'Mi', 'Gi']

		bars = f"{bar}"
		pers = f"{percents:5.1f}%"
		size = f"{currentSize:6.2f}{pref[i]}B"
		pers = f"{pers:>6}"
		size = f"{size:>9}"

		return f"{bars} {pers} {size}\r"



