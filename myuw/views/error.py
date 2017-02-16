import sys
from django.http import HttpResponse
from restclients.exceptions import (DataFailureException, InvalidNetID,
                                    InvalidRegID)
from myuw.logger.logresp import log_err


HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405
HTTP_GONE = 410
MYUW_DATA_ERROR = 543


def _make_response(status_code, reason_phrase):
    response = HttpResponse(reason_phrase)
    response.status_code = status_code
    response.reason_phrase = reason_phrase
    return response


def invalid_session():
    return _make_response(HTTP_BAD_REQUEST, "No valid userid in session")


def invalid_term():
    return _make_response(HTTP_BAD_REQUEST, "Invalid requested term")


def data_not_found():
    return _make_response(HTTP_NOT_FOUND, "Data not found")


def invalid_method():
    return _make_response(HTTP_METHOD_NOT_ALLOWED, "Method not allowed")


def invalid_future_term():
    return _make_response(HTTP_GONE, "Invalid requested future term")


def data_error():
    return _make_response(MYUW_DATA_ERROR,
                          "Data not available due to an error")


def handle_exception(logger, timer, stack_trace):
    log_err(logger, timer, stack_trace.format_exc())
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if isinstance(exc_value, InvalidNetID) or\
            isinstance(exc_value, InvalidRegID):
        return invalid_session()
    if isinstance(exc_value, DataFailureException) and\
            exc_value.status == 404:
        return data_not_found()
    return data_error()
