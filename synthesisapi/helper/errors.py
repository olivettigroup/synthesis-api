# Python class holding the different error types that could be returned
# by the API

class ErrorFactory:
    structure = ['error_type' 
                 'message']

    default = {'error_type': 'Invalid',
               'message': 'Invalid'}

    error_types = [ 0: 'Invalid',
                    1: 'Invalid Input']

    def makeError(error_type, message):
        if error_types[error_type]:
            return

