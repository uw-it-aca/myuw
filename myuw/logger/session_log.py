# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import hashlib
import json
import logging
from django_user_agents.utils import get_user_agent
from myuw.dao import get_userids
from myuw.dao.affiliation import get_all_affiliations

logger = logging.getLogger('session')


def log_session(request):
    logger.info({**get_userids(request),
                 **_get_session_data(request),
                 **_get_affi(request)})


def log_session_end(request):
    logger.info({**get_userids(request),
                 **{'msg': 'logout',
                    'session_key': hash_session_key(request),
                    'is_native': is_native(request)}})


def _get_session_data(request):
    return {'session_key': hash_session_key(request),
            'ip': get_ip(request),
            'is_mobile': is_mobile(request),
            'is_native': is_native(request)}


def _get_affi(request):
    affiliations = get_all_affiliations(request)
    return {'class_level': affiliations["class_level"],
            'hxt_viewer': affiliations["hxt_viewer"],
            'applicant': affiliations["applicant"],
            'ugrad': affiliations["undergrad"],
            'grad': affiliations["grad"],
            'pce': affiliations["pce"],
            'student': affiliations["student"],
            'grad_c2': affiliations["grad_c2"],
            'undergrad_c2': affiliations["undergrad_c2"],
            'intl_stud': affiliations["intl_stud"],
            'employee': affiliations["employee"],
            'stud_employee': affiliations["stud_employee"],
            'staff': affiliations["staff_employee"],
            'faculty': affiliations["faculty"],
            'instructor': affiliations["instructor"],
            'alumni': affiliations["alumni"],
            'clinician': affiliations["clinician"],
            'retired_staff': affiliations["retiree"],
            'past_employee': affiliations["past_employee"],
            'past_stud': affiliations["past_stud"],
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


def is_mobile(request):
    try:
        user_agent = get_user_agent(request)
        return user_agent.is_mobile or user_agent.is_tablet
    except Exception as ex:
        logger.warning("is_mobile ==> {}".format(str(ex)))
    return ""


def is_native(request):
    try:
        ua_string = request.META['HTTP_USER_AGENT']
    except KeyError:
        ua_string = ""
    return 'MyUW_Hybrid' in ua_string
