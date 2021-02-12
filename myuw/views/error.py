import sys
from django.http import HttpResponse
from restclients_core.exceptions import (
    DataFailureException, InvalidNetID, InvalidRegID)
from myuw.dao.exceptions import (
    NotSectionInstructorException, InvalidResourceCategory)
from myuw.models import ResourceCategoryPin
from uw_sws.exceptions import InvalidSectionID, ThreadedDataError
from myuw.logger.logresp import log_err, log_data_not_found_response
from myuw.views.exceptions import (
    DisabledAction, NotInstructorError, InvalidInputFormData)


HTTP_BAD_REQUEST = 400
UNAUTHORIZED_ERROR = 403
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405
HTTP_GONE = 410
MYUW_DATA_ERROR = 543


def _make_response(status_code, reason_phrase):
    response = HttpResponse(reason_phrase)
    response.status_code = status_code
    response.reason_phrase = reason_phrase
    return response


def disabled_action_error():
    return _make_response(UNAUTHORIZED_ERROR,
                          "Action Disabled while overriding users")


def no_access():
    return _make_response(
        UNAUTHORIZED_ERROR,
        "<p>This is a test environment of MyUW, "
        "its access is limited to specific people. "
        "To request access, please contact the "
        "<a href=\"https://itconnect.uw.edu/it-connect-home/question/\">"
        "UW-IT Service Center</a>.</p>")


def not_instructor_error():
    return _make_response(UNAUTHORIZED_ERROR,
                          "Access Forbidden to Non Instructor")


def blocked_uwnetid():
    return _make_response(
        UNAUTHORIZED_ERROR,
        "<p>MyUW encountered a problem with your uwnetid, please contact the "
        "<a href=\"https://itconnect.uw.edu/it-connect-home/question/\">"
        "UW-IT Service Center</a>.</p>")


def unknown_uwnetid():
    return _make_response(
        UNAUTHORIZED_ERROR,
        "<p>MyUW cannot find data for this user account "
        "in the Person Registry services. "
        "If you have just created your UW NetID, "
        "please try signing in to MyUW again in one hour.</p>")


def pws_error_404():
    return _make_response(
        UNAUTHORIZED_ERROR,
        "<p>MyUW cannot find data for this user account "
        "in the Person Registry services. Please contact the "
        "<a href=\"https://itconnect.uw.edu/it-connect-home/question/\">"
        "UW-IT Service Center</a>.</p>")


def invalid_input_data():
    return _make_response(HTTP_BAD_REQUEST, "Invalid post data content")


def invalid_section():
    return _make_response(HTTP_BAD_REQUEST, "Invalid section label")


def not_section_instructor():
    return _make_response(HTTP_BAD_REQUEST, "Invalid section instructor")


def data_not_found():
    return _make_response(HTTP_NOT_FOUND, "Data not found")


def invalid_method():
    return _make_response(HTTP_METHOD_NOT_ALLOWED, "Method not allowed")


def invalid_future_term(msg):
    return _make_response(HTTP_GONE,
                          "Invalid requested future term {}".format(msg))


def data_error():
    return _make_response(MYUW_DATA_ERROR,
                          "Data not available due to an error")


def handle_exception(logger, timer, stack_trace):
    exc_type, exc_value, exc_traceback = sys.exc_info()

    if (isinstance(exc_value, DataFailureException) and
            not isinstance(exc_value, ThreadedDataError) and
            (exc_value.status == 400 or exc_value.status == 404)):
        log_data_not_found_response(logger, timer)
        return data_not_found()

    log_err(logger, timer, stack_trace)

    if isinstance(exc_value, DisabledAction):
        return disabled_action_error()

    if isinstance(exc_value, NotInstructorError):
        return not_instructor_error()

    if isinstance(exc_value, InvalidNetID) or\
       isinstance(exc_value, InvalidRegID):
        return unknown_uwnetid()

    if (isinstance(exc_value, InvalidInputFormData) or
            isinstance(exc_value, InvalidResourceCategory) or
            isinstance(exc_value, ResourceCategoryPin.DoesNotExist)):
        return invalid_input_data()

    if isinstance(exc_value, InvalidSectionID):
        return invalid_section()

    if isinstance(exc_value, NotSectionInstructorException):
        return not_section_instructor()

    return data_error()
