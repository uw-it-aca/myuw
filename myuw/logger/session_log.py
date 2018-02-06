import logging
import json
import hashlib
from myuw.dao.affiliation import get_all_affiliations, get_base_campus
from myuw.dao.enrollment import get_current_quarter_enrollment

logger = logging.getLogger('session')


def log_session(netid, affiliations, session_key, request):
    if session_key is None:
        session_key = ''

    if affiliations is None:
        affiliations = get_all_affiliations(request)

    session_hash = hashlib.md5(session_key.encode('utf-8')).hexdigest()
    log_entry = {'netid': netid,
                 'session_key': session_hash,
                 'class_level': None,
                 'is_grad': affiliations["grad"],
                 'is_ugrad': affiliations["undergrad"],
                 'is_pce': affiliations["pce"],
                 'is_student': affiliations["student"],
                 'is_staff': affiliations["staff_employee"],
                 'is_faculty': affiliations["faculty"],
                 'is_instructor': affiliations["instructor"],
                 'is_employee': affiliations["employee"],
                 'is_applicant': affiliations["applicant"],
                 'is_alumni': affiliations["alumni"],
                 'is_clinician': affiliations["clinician"],
                 'sea_campus': affiliations['official_seattle'],
                 'bot_campus': affiliations['official_bothell'],
                 'tac_campus': affiliations['official_tacoma'],
                 }
    try:
        level = get_current_quarter_enrollment(request).class_level
        log_entry['class_level'] = level
        is_mobile = request.is_mobile or request.is_tablet
        log_entry['is_mobile'] = bool(is_mobile)
    except Exception:
        pass

    try:
        log_entry['campus'] = get_base_campus(request)
    except Exception:
        pass
    logger.info(json.dumps(log_entry))
