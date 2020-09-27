from pathlib import Path
from layers.lib import Layer, Exceptions
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# Represents a set of layers in a layer set
class LayerSet:
	@classmethod
	def fromLayer(cls, layer: Layer):
		return cls(Layer(layer.config.path.resolve().parent))

	def __init__(self, baseLayer: Layer):
		self.baseLayer = baseLayer

	# Remove a file (or directory) from the entire layer set
	def rm(self, lpath: Path):
		pass

	@property
	def layers(self):
		return self.baseLayer.layers

	@property
	def path(self):
		return self.baseLayer.path

	@property
	def files(self):
		# All the files in this layerset
		files = []
		for layer in self.layers:
			files.extend(layer.files)
		return files

	# Sync the entire layer set
	def sync(self):
		logger.debug(f"Syncing {len(self.files)} files in {len(self.layers)} layers")
		files = self.files
		for f in files:
			logger.debug(f"- {f.localPath} from {f.layer.path}")
			for layer in self.layers:
				if layer == f.layer:
					continue
				
				logger.debug(f"- to {layer.path}")
				if f.inLayer(layer).path.exists():
					if f.inLayer(layer).path.resolve().samefile(f.path.resolve()):
						# Allready linked, we good
						continue
					else:
						raise Exceptions.FileConflictError(f"Conflicting content between layer {layer.level}@{layer.path} and {f.layer.level}@{f.layer.path} for file {f.localPath}")
				else:
					# If the destination does not contain the parent
					# diretory this file is in, then we symlink the entire directory.
					p = f
					while not p.inLayer(layer).path.parent.exists():
						p = p.parent
					p.inLayer(layer).path.symlink_to(p.path)

	# Purge the entire layer set
	def purge(self):
		for layer in self.baseLayer.layers:
			layer.purge()

	# Merge layerset into target and remove the layers (Except the target)
	def merge(self, target: Path):
		pass