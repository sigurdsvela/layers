class LayersError(OSError):
    pass

class NotALayerDirectoryError(LayersError):
    pass

class UnsafeOnOriginalError(LayersError):
    pass

class FileConflictError(LayersError):
    pass

class NotALayerSetError(LayersError):
    pass

class InvalidArgumentError(TypeError):
    def __init__(self, argValue, argType, message=""):
        super().__init__(message)
        self._argValue = argValue
        self._argType = argType
    
    @property
    def argValue(self):
        return self._argValue

    @property
    def argType(self):
        return self._argType
