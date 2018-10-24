import hashlib
import json
import logging
from django_user_agents.utils import get_user_agent
from myuw.dao import get_netid_of_original_user, get_netid_of_current_user
from myuw.dao.affiliation import get_all_affiliations

logger = logging.getLogger('session')


def log_session(request):
    data = {'session_key': hash_session_key(request),
            'ip': get_ip(request),
            'is_mobile': is_mobile(request),
            'referer': request.META.get('HTTP_REFERER')}
    logger.info("{}, {}, {}".format(get_userid(), json.dumps(data),
                                    json.dumps(_get_affi(request))))


def _get_affi(request):
    affiliations = get_all_affiliations(request)
    return {'class_level': affiliations["class_level"],
            'fyp': affiliations["fyp"],
            'fyp': affiliations["fyp"],
            'aut_transfer': affiliations["aut_transfer"],
            'win_transfer': affiliations["win_transfer"],
            'hxt_viewer': affiliations["hxt_viewer"],
            'is_applicant': affiliations["applicant"],
            'is_ugrad': affiliations["undergrad"],
            'is_grad': affiliations["grad"],
            'is_pce': affiliations["pce"],
            'is_student': affiliations["student"],
            'grad_c2': affiliations["grad_c2"],
            'undergrad_c2': affiliations["undergrad_c2"],
            'intl_stud': affiliations["intl_stud"],
            'is_employee': affiliations["employee"],
            'is_staff': affiliations["staff_employee"],
            'is_faculty': affiliations["faculty"],
            'is_instructor': affiliations["instructor"],
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
            'tac_emp': affiliations.get('official_tacoma', False)}


def hash_session_key(request):
    try:
        session_key = request.session.session_key
        return hashlib.md5(session_key.encode('utf8')).hexdigest()
    except Exception:
        pass
    return ""


def get_ip(request):
    try:
        x_forwarded_for = request.META.get('X-Forwarded-For')
        if x_forwarded_for:
            # originating-ip
            return x_forwarded_for  # .split(',')[0]
        else:
            return request.META.get('REMOTE_ADDR')
    except Exception as ex:
        logger.warning("ip ==> {}".format(str(ex)))
    return ""


def get_userid():
    """
    Return <actual user netid> acting_as: <override user netid> if
    the user is acting as someone else, otherwise
    <actual user netid> no_override: <actual user netid>
    """
    override_userid = get_netid_of_current_user()
    actual_userid = get_netid_of_original_user()
    log_format = 'orig_netid: {}, acting_netid: {}, is_override: {}'
    try:
        return log_format.format(actual_userid,
                                 override_userid,
                                 override_userid != actual_userid)
    except Exception as ex:
        logger.warning("get_userid ==> {}".format(str(ex)))
    return ""


def is_mobile(request):
    try:
        user_agent = get_user_agent(request)
        return user_agent.is_mobile or user_agent.is_tablet
    except Exception as ex:
        logger.warning("is_mobile ==> {}".format(str(ex)))
    return ""
