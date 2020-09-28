from pathlib import Path


def PathInLayer(arg):
	import os
	from pathlib import Path
	from layers.lib import LayerLocalPath, Layer, Exceptions

	path = Path(arg)
	path = path.absolute()

	try:
		llpath = LayerLocalPath(Layer.findRoot(path), path.absolute())
	except Exceptions.NotALayerDirectoryError as e:
		print(e)
		return None
	return llpath


def level(target_layer:Path, target_file: Path):
	from layers.lib import Layer, LayerLocalPath
	def mapper(arg):
		max_level = len(Layer(target_layer.absolute()).layers)-1
		if isinstance(arg, int):
			return max(min(arg, max_level), 0)
		elif arg == 'top':
			return 0
		elif arg == 'bottom':
			return max_level
		elif arg == 'down':
			return min(LayerLocalPath(target_file.resolve().absolute()).layer.level + 1, max_level)
		elif arg == 'up':
			return max(LayerLocalPath(target_file.resolve().absolute()).layer.level - 1, 0)
	return mapper