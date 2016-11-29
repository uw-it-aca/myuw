import json
import sys
from django.http import HttpResponse
from userservice.user import UserService
from restclients.exceptions import DataFailureException,\
    InvalidNetID, InvalidRegID
from myuw.logger.logresp import log_err, log_data_not_found_response


class RESTDispatch(object):
    """
    Handles passing on the request to the correct view
    method based on the request type.
    """
    def run(self, *args, **named_args):
        request = args[0]

        user_service = UserService()
        netid = user_service.get_user()
        if not netid:
            return invalid_session()

        if "GET" == request.META['REQUEST_METHOD']:
            if hasattr(self, "GET"):
                return self.GET(*args, **named_args)
            else:
                return invalid_method()
        elif "POST" == request.META['REQUEST_METHOD']:
            if hasattr(self, "POST"):
                return self.POST(*args, **named_args)
            else:
                return invalid_method()
        elif "PUT" == request.META['REQUEST_METHOD']:
            if hasattr(self, "PUT"):
                return self.PUT(*args, **named_args)
            else:
                return invalid_method()
        elif "DELETE" == request.META['REQUEST_METHOD']:
            if hasattr(self, "DELETE"):
                return self.DELETE(*args, **named_args)
            else:
                return invalid_method()

        else:
            return invalid_method()


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


def _make_response(status_code, reason_phrase):
    response = HttpResponse(reason_phrase)
    response.status_code = status_code
    response.reason_phrase = reason_phrase
    return response


def invalid_session():
    return _make_response(400, "No valid userid in session")


def invalid_term():
    return _make_response(400, "Invalid requested term")


def data_not_found():
    return _make_response(404, "Data not found")


def invalid_method():
    return _make_response(405, "Method not allowed")


def invalid_future_term():
    return _make_response(410, "Invalid requested future term")


def data_error():
    return _make_response(543, "Data not available due to an error")
