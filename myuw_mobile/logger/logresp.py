from myuw_mobile.dao.gws import Member
from myuw_mobile.logger.logback import log_time

def log_response_time(logger, message, timer):
    log_time(logger, message, timer) 

def log_success_response(logger, timer):
    log_time(logger, 
             get_identity() + 'fulfilled', 
             timer) 

def log_data_not_found_response(logger, timer):
    log_time(logger,
             get_identity() + ' data not found',
             timer)

def log_invalid_netid_response(logger, timer):
    log_time(logger, 'invalid netid, abort', timer)

def log_invalid_regid_response(logger, timer):
    log_time(logger, 'invalid regid, abort', timer)

def get_identity():
    """
    Return "(Affiliations: <affiliations>, <campus codes>)"
    """
    res = "(Affiliations:"
    member = Member()
    if member.is_grad_student():
        res += ' Grad'
    if member.is_undergrad_student():
        res += ' Undergrad'
    if member.is_pce_student():
        res += ' Pce'
    if member.is_student_employee():
        res += ' StudEmployee'
    if len(res) > 16:
        res += ','
    if member.is_seattle_student():
        res += ' Seattle'
    if member.is_bothell_student():
        res += ' Bothell'
    if member.is_tacoma_student():
        res += ' Tacoma'
    if len(res) < 16:
        res += 'None'
    res += ') '
    return res

