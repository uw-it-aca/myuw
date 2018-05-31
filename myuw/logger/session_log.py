import hashlib
import json
import logging
from myuw.dao import is_using_file_dao
from myuw.dao.affiliation import get_all_affiliations, get_base_campus

logger = logging.getLogger('session')


def log_session(netid, request):
    affiliations = get_all_affiliations(request)
    log_entry = {'netid': netid,
                 'session_key': get_request_session_key(request),
                 'class_level': affiliations["class_level"],
                 'is_applicant': affiliations["applicant"],
                 'is_ugrad': affiliations["undergrad"],
                 'is_grad': affiliations["grad"],
                 'is_pce': affiliations["pce"],
                 'undergrad_c2': affiliations["undergrad_c2"],
                 'grad_c2': affiliations["grad_c2"],
                 'fyp': affiliations["fyp"],
                 'aut_transfer': affiliations["aut_transfer"],
                 'win_transfer': affiliations["win_transfer"],
                 'is_student': affiliations["student"],
                 'is_staff': affiliations["staff_employee"],
                 'is_faculty': affiliations["faculty"],
                 'is_instructor': affiliations["instructor"],
                 'is_employee': affiliations["employee"],
                 'is_alumni': affiliations["alumni"],
                 'is_clinician': affiliations["clinician"],
                 'is_retired_staff': affiliations["retiree"],
                 'is_past_employee': affiliations["past_employee"],
                 'is_past_stud': affiliations["past_stud"],
                 'sea_campus': affiliations['official_seattle'],
                 'bot_campus': affiliations['official_bothell'],
                 'tac_campus': affiliations['official_tacoma'],
                 }
    try:
        is_mobile = request.is_mobile or request.is_tablet
        log_entry['is_mobile'] = bool(is_mobile)
    except Exception:
        pass

    try:
        x_forwarded_for = request.META.get('X-Forwarded-For')
        if x_forwarded_for:
            log_entry['originating-ip'] = x_forwarded_for  # .split(',')[0]
        else:
            log_entry['client_ip'] = request.META.get('REMOTE_ADDR')
    except Exception:
        pass

    try:
        log_entry['campus'] = get_base_campus(request)
    except Exception:
        pass
    logger.info(json.dumps(log_entry))


def get_request_session_key(request):
    if is_using_file_dao():
        return ""
    session_key = request.session.session_key
    return hashlib.md5(session_key.encode('utf-8')).hexdigest()
