class LayersError(OSError):
    pass

class NotALayerDirectoryError(LayersError):
    pass

class FileConflictError(LayersError):
    pass


        