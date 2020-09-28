class LayersError(OSError):
    pass

class NotALayerDirectoryError(LayersError):
    pass

class UnsafeOnOriginalError(LayersError):
    pass

class FileConflictError(LayersError):
    pass


        