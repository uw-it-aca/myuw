from myuw.dao.affiliation import get_base_campus
from myuw.dao.enrollment import get_current_quarter_enrollment
from myuw.dao.gws import is_grad_student, is_undergrad_student
import logging
import json
import hashlib

logger = logging.getLogger('session')


def log_session(netid, session_key, request):
    if session_key is None:
        session_key = ''

    session_hash = hashlib.md5(session_key).hexdigest()
    log_entry = {'netid': netid,
                 'session_key': session_hash,
                 'class_level': None,
                 'is_grad': None,
                 'campus': None}
    try:
        level = get_current_quarter_enrollment(request).class_level
        log_entry['class_level'] = level
    except AttributeError:
        pass
    log_entry['is_grad'] = is_grad_student()
    log_entry['is_ugrad'] = is_undergrad_student()
    log_entry['campus'] = get_base_campus(request)

    logger.info(json.dumps(log_entry))
