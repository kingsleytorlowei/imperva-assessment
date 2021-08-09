from flask import Response
from functools import wraps
import json

class ImpervaBadRequest(Exception):
    pass

class ImpervaNotFound(Exception):
    pass

class ImpervaError(Exception):
    pass


class ErrorResponse:

    RESPONSE_STATUS_CODES = {
        400 : 400,
        403 : 403,
        404 : 404,
        500 : 500,
        }

    RESPONSE_STATUS = {
        400 : 'BAD_REQUEST',
        403 : 'FORBIDDEN',
        404 : 'NOT_FOUND',
        500 : 'INTERNAL_SERVER_ERROR',
        }

    @staticmethod
    def response(message, code):
        http_status_code = ErrorResponse.RESPONSE_STATUS_CODES[code]
        http_status = ErrorResponse.RESPONSE_STATUS[code]
        response_message = json.dumps({'status': http_status, 'error code': http_status_code,'message': f'{message}'})
        return Response(
            response_message,
            status = http_status_code,
            mimetype='application/json'
            )

def http_error(f):
    @wraps(f)
    def function_impl(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except KeyError as e:
            print(str(e))
            return ErrorResponse.response(f'KeyError: {str(e)} missing', 400)
        except ImpervaBadRequest as e:
            print(str(e))
            return ErrorResponse.response(str(e), 400)
        except ImpervaNotFound as e:
            print(str(e))
            return ErrorResponse.response(str(e), 404)
        except ImpervaError as e:
            print(str(e))
            return ErrorResponse.response(str(e), 500)
        except Exception as e:
            print(str(e))
            return ErrorResponse.response(str(e), 500)

    return function_impl
