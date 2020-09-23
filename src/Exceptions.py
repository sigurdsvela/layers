
class InvalidLayersPathException(Exception):
        def __init__(self, expression = "Not a layerset", message = "The path is not in a layersset"):
                self.expression = expression
                self.message = message


class FileConflictException(Exception):
        def __init__(self, expression = "File conflict", message = "A file was found in multiple places"):
                self.expression = expression
                self.message = message

class LinkException(Exception):
        def __init__(self, message):
                self.message = message

	