from myuw.dao.affiliation import get_all_affiliations
from myuw.logger.logback import log_info, log_time, log_exception_with_timer


def log_response_time(logger, message, timer):
    log_time(logger, message, timer)


def log_success_response(logger, timer):
    log_time(logger, 'fulfilled', timer)


def log_success_response_with_affiliation(logger, timer, request):
    log_time(logger,
             get_identity(request) + 'fulfilled',
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


def get_identity(request):
    """
    Return "(Affiliations: <affiliations>, <campus codes>)"
    """
    res = "(Affiliations:"
    no_affiliation_lengthmark = len(res)
    affi = get_all_affiliations(request)
    if affi["grad"]:
        res += ' Grad'
    if affi["undergrad"]:
        res += ' Undergrad'
    if affi["pce"]:
        res += ' Pce'
    if affi["employee"]:
        res += ' Employee'
    if affi["faculty"]:
        res += ' Faculty'
    if len(res) == no_affiliation_lengthmark:
        res += 'None'
    res += ', Campuses:'
    no_campus_lengthmark = len(res)
    if affi["seattle"]:
        res += ' Seattle'
    if affi["bothell"]:
        res += ' Bothell'
    if affi["tacoma"]:
        res += ' Tacoma'
    if len(res) == no_campus_lengthmark:
        res += 'None'
    res += ') '
    return res
