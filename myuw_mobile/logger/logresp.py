from myuw_mobile.dao.affiliation import get_all_affiliations
from myuw_mobile.logger.logback import log_info, log_time


def log_response_time(logger, message, timer):
    log_time(logger, message, timer)


def log_success_response(logger, timer):
    log_time(logger, 'fulfilled', timer)


def log_success_response_with_affiliation(logger, timer):
    log_time(logger,
             get_identity() + 'fulfilled',
             timer)


def log_data_not_found_response(logger, timer):
    log_time(logger,
             ' data not found',
             timer)


def log_invalid_netid_response(logger, timer):
    log_time(logger, 'invalid netid, abort', timer)


def log_invalid_regid_response(logger, timer):
    log_time(logger, 'invalid regid, abort', timer)


def log_affiliation(logger, message):
    log_info(logger, get_identity() + message)


def get_identity():
    """
    Return "(Affiliations: <affiliations>, <campus codes>)"
    """
    res = "(Affiliations:"
    no_affiliation_lengthmark = len(res)
    affi = get_all_affiliations()
    if affi["grad"]:
        res += ' Grad'
    if affi["undergrad"]:
        res += ' Undergrad'
    if affi["pce"]:
        res += ' Pce'
    if affi["stud_employee"]:
        res += ' StudEmployee'
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
