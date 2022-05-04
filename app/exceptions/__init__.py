from werkzeug.exceptions import BadRequest

class InvalidDataTypeError(BadRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)