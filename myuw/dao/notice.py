# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the interactions with
the SWS notice resource.
"""

import logging
from django.db import IntegrityError
from uw_sws.notice import get_notices_by_regid
from myuw.models import UserNotices
from myuw.dao.category_notice import get_category_notices
from myuw.dao.enrollment import get_latest_class_level
from myuw.dao.instructor import is_instructor
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.notice_mapping import categorize_notices
from myuw.dao.user import get_user_model
from myuw.dao.myuw_notice import get_myuw_notices_for_user
from myuw.dao.pws import is_student
from myuw.dao.term import within_grading_period

logger = logging.getLogger(__name__)


def _get_notices_by_regid(user_regid):
    """
    returns SWS notices for a given regid with
    myuw specific categories
    """

    if user_regid is None:
        return None

    notices = get_notices_by_regid(user_regid)
    if notices is None:
        return None
    return categorize_notices(notices)


def mark_notices_read_for_current_user(request, notice_hashes):
    user = get_user_model(request)
    UserNotices().mark_notices_read(notice_hashes, user)


def get_notices_for_current_user(request):
    notices = []
    if is_instructor(request):
        # MUWM-5199
        notices += categorize_notices(get_category_notices("Teaching"))

        # MUWM-4072
        if within_grading_period(request):
            notices += categorize_notices(
                get_category_notices("GradeSubmission"))

    if is_student(request):
        notices += _get_notices_by_regid(get_regid_of_current_user(request))

        # MUWM-5065
        class_level = get_latest_class_level(request)
        if class_level and class_level.upper() == 'SENIOR':
            notices += categorize_notices(get_category_notices("Degree"))

    notices += categorize_notices(get_myuw_notices_for_user(request))
    return _get_user_notices(request, notices)


def _get_user_notices(request, notices):
    user = get_user_model(request)
    notice_dict = {}
    notices_with_read_status = []
    # Get all notice hashes
    for notice in notices:
        notice_hash = UserNotices().generate_hash(notice)
        notice.id_hash = notice_hash
        notice.is_read = False
        notice_dict[notice_hash] = notice

    # Set read status for notices already in db
    keys = notice_dict.keys()
    user_notices = UserNotices.objects.filter(user=user,
                                              notice_hash__in=keys)
    for user_notice in user_notices:
        matched_notice = notice_dict[user_notice.notice_hash]
        matched_notice.is_read = user_notice.is_read
        notices_with_read_status.append(matched_notice)
        del notice_dict[user_notice.notice_hash]

    # Create UserNotices for new notices
    for notice in notice_dict.values():
        user_notice, _ = UserNotices.objects.get_or_create(
            notice_hash=notice.id_hash, user=user, defaults={
                'notice_cattype': notice.notice_category + notice.notice_type,
        })
        notices_with_read_status.append(user_notice)

    return notices_with_read_status
