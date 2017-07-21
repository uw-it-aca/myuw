from myuw.dao.affiliation import get_identity_log_str
from myuw.logger.logback import log_info, log_time, log_exception_with_timer


def log_response_time(logger, message, timer):
    log_time(logger, message, timer)


def log_success_response(logger, timer):
    log_time(logger, 'fulfilled', timer)


def log_success_response_with_affiliation(logger, timer, request):
    log_time(logger,
             get_identity_log_str(request) + 'fulfilled',
             timer)


def log_msg_with_affiliation(logger, timer, request, msg):
    log_time(logger,
             "%s %s" % (get_identity_log_str(request), msg),
             timer)


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
