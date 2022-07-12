from .error_handler import ApiError


def throw(msg=None, code=500):
    if not msg:
        if code == 500:
            msg = 'Server Error'
        elif code == 410:
            msg = 'Resource Deleted'
        elif code == 404:
            msg = 'Not Found'
        elif code == 401:
            msg = 'Unauthorized Request'
        elif code == 403:
            msg = 'Forbidden Request'
        elif code == 422:
            msg = 'Unprocessable Request'

    raise ApiError(msg, code)
