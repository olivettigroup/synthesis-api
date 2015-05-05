# Python class holding the different error types that could be returned
# by the API

class ErrorFactory:
    structure = {'error_type': None
                 'message': None
                 }

    default = {'error_type': 'Invalid',
               'message': 'Invalid'}

    error_types = { 0: 'Invalid',
                    1: 'Invalid Input'
                    2: 'Database Error'}

    def makeError(error_type, message):
        if not error_types[error_type]:
            return -1
        result = structure.copy()
        result['error_type'] = error_types[error_type]
        result['message'] = message

        return result
