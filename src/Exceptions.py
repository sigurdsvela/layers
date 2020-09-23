
class InvalidLayersPathException(Exception):
        def __init__(self, expression = "Not a layerset", message = "The path is not in a layersset"):
                self.expression = expression
                self.message = message

	