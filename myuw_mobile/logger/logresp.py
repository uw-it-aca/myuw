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
    Return "(<affiliation codes>, <campus codes>)"
    """
    res = " ("
    member = Member()
    if member.is_grad_student():
        res += 'G'
    if member.is_undergrad_student():
        res += 'U'
    if member.is_pce_student():
        res += 'P'
    if member.is_student_employee():
        res += 'E'
    res += ','
    if member.is_seattle_student():
        res += 'S'
    if member.is_bothell_student():
        res += 'B'
    if member.is_tacoma_student():
        res += 'T'
    res += ') '
    return res

