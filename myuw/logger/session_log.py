import hashlib
import json
import logging
from myuw.dao import is_using_file_dao
from myuw.dao.affiliation import get_all_affiliations

logger = logging.getLogger('session')


def log_session(netid, request):
    logger.info(json.dumps(get_log_entry(netid, request)))


def get_log_entry(netid, request):
    affiliations = get_all_affiliations(request)
    log_entry = {'netid': netid,
                 'session_key': get_request_session_key(request),
                 'referer': request.META.get('HTTP_REFERER'),
                 'class_level': affiliations["class_level"],
                 'is_applicant': affiliations["applicant"],
                 'is_ugrad': affiliations["undergrad"],
                 'is_grad': affiliations["grad"],
                 'is_pce': affiliations["pce"],
                 'undergrad_c2': affiliations["undergrad_c2"],
                 'grad_c2': affiliations["grad_c2"],
                 'intl_stud': affiliations["intl_stud"],
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
                 'sea_stud': affiliations.get('seattle', False),
                 'bot_stud': affiliations.get('bothell', False),
                 'tac_stud': affiliations.get('tacoma', False),
                 'sea_emp': affiliations.get('official_seattle', False),
                 'bot_emp': affiliations.get('official_bothell', False),
                 'tac_emp': affiliations.get('official_tacoma', False),
                 }
    try:
        is_mobile = request.is_mobile or request.is_tablet
        log_entry['is_mobile'] = bool(is_mobile)
    except Exception as ex:
        logger.warning("is_mobile ==> %s" % ex)
        pass

    try:
        x_forwarded_for = request.META.get('X-Forwarded-For')
        if x_forwarded_for:
            # originating-ip
            log_entry['ip'] = x_forwarded_for  # .split(',')[0]
        else:
            log_entry['ip'] = request.META.get('REMOTE_ADDR')
    except Exception as ex:
        logger.warning("ip ==> %s" % ex)
        pass
    return log_entry


def get_request_session_key(request):
    if is_using_file_dao():
        return ""
    session_key = request.session.session_key
    return hashlib.md5(session_key.encode('utf8')).hexdigest()
