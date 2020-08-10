from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def bad_request(message):
    """
    The most common error that the API is going to return is going to be
    the code 400, which is the error for "bad request".
    """
    return error_response(400, message)


def error_response(status_code, message=None) -> dict:
    """
    Return request's response in case of error.
    :status_code:
    :message:
    HTTP_STATUS_CODES provides a short descriptive name for each HTTP status
    code.

    :return: dict
    """
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response
