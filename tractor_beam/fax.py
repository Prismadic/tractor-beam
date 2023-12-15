from .utils import _f

class Fax:
    def __init__(self, data=None):
        """
        The function initializes an object with a data attribute and raises a fatal error if no data is
        passed.
        
        :param data: The "data" parameter is used to pass a value to the "self.data" attribute of the
        class. It is an optional parameter, meaning it can be omitted when creating an instance of the
        class. If no value is passed for "data", a fatal error message will be logged with the message
        """
        self.data = data 
        _f('fatal', 'no data passed to send') if data is None else None