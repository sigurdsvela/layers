def PathInLayer(arg):
	import os
	from pathlib import Path
	from layers.lib import LayerLocalPath, Layer, Exceptions

	path = Path(arg)
	path = path.absolute()

	try:
		llpath = LayerLocalPath(Layer.findRoot(path), path.absolute())
	except Exceptions.NotInLayerError as e:
		print(e)
		return None
	return llpath
