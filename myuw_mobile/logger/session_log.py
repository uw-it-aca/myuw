from myuw_mobile.dao.affiliation import get_base_campus
from myuw_mobile.dao.enrollment import get_current_quarter_enrollment
from myuw_mobile.dao.gws import is_grad_student, is_undergrad_student
import logging
import json

logger = logging.getLogger('session')


def log_session(netid, session_key, request):
    log_entry = {'netid': netid,
                 'session_key': session_key,
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
