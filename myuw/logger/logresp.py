from myuw.logger.logback import log_info, log_time, log_exception_with_timer
from myuw.logger.session_log import get_request_session_key


def log_msg_with_request(logger, timer, request, msg='fulfilled'):
    if timer:
        log_time(logger,
                 "session_key:%s, %s" % (
                     get_request_session_key(request), msg),
                 timer)
    else:
        log_info(logger,
                 "session_key:%s, %s" % (get_request_session_key(request),
                                         msg))


def log_success_response(logger, timer):
    log_time(logger, 'fulfilled', timer)


def log_err(logger, timer, exc_info):
    """
    exc_info is a string containing
    the full stack trace, the exception type and value
    """
    log_exception_with_timer(logger, timer, exc_info)


def log_msg(logger, timer, msg):
    log_time(logger, msg, timer)


def log_data_not_found_response(logger, timer):
    log_time(logger, 'Data not found', timer)


def log_invalid_netid_response(logger, timer):
    log_time(logger, 'Invalid netid, abort', timer)


def log_invalid_regid_response(logger, timer):
    log_time(logger, 'Invalid regid, abort', timer)
