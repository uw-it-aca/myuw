# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the interactions with
the SWS Personal Financial resource.
"""

import logging
import traceback
from uw_libraries.mylib import get_account
from uw_libraries.subject_guides import (
    get_subject_guide_for_section, get_default_subject_guide)
from restclients_core.exceptions import DataFailureException
from myuw.dao import log_err
from myuw.dao.pws import get_netid_of_current_user


logger = logging.getLogger(__name__)


def _get_account_by_uwnetid(uwnetid):
    """
    returns uw_libraries.models.MyLibAccount object
    for a given uwnetid
    """
    if uwnetid is None:
        return None
    return get_account(uwnetid)


def get_account_info_for_current_user(request):
    return _get_account_by_uwnetid(get_netid_of_current_user(request))


def get_subject_guide_by_section(section):
    """
    returns a url string
    """
    if section is None:
        return None
    get_default = False
    section_campus = section.course_campus.lower()
    section_logid = "({} {} {}, {})".format(section.curriculum_abbr,
                                            section.course_number,
                                            section.section_id,
                                            section_campus)
    try:
        subject_guide = get_subject_guide_for_section(section)
        if subject_guide.is_default_guide:
            default_campus = subject_guide.default_guide_campus.lower()
            if default_campus != section_campus:
                get_default = True
    except DataFailureException as ex:
        if ex.status == 404:
            get_default = True
        else:
            log_err(logger, "get_subject_guide for {}".format(section_logid),
                    traceback, None)
            raise

    if get_default:
        subject_guide = get_default_subject_guide(section_campus)

    return subject_guide.guide_url


def library_resource_prefetch():
    def build_method(campus):
        def _method(request):
            get_default_subject_guide(campus)
        return _method

    methods = []
    for campus in ['seattle', 'tacoma', 'bothell']:
        methods.append(build_method(campus))
    return methods
