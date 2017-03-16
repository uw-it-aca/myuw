"""
This class encapsulates the interactions with
the SWS notice resource.
"""

import logging
from django.db import IntegrityError
from uw_sws.notice import get_notices_by_regid
from myuw.models import TuitionDate, UserNotices
from myuw.dao import get_user_model
from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.notice_mapping import categorize_notices


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


def mark_notices_read_for_current_user(notice_hashes):
    user = get_user_model()
    UserNotices().mark_notices_read(notice_hashes, user)


def get_notices_for_current_user():
    notices = _get_notices_by_regid(get_regid_of_current_user())
    return _get_user_notices(notices)


def _get_user_notices(notices):
    user = get_user_model()
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
    user_notices_to_create = []
    for notice in notice_dict.values():
        user_notice = UserNotices()
        user_notice.notice_hash = notice.id_hash
        user_notice.user = user
        cattype = notice.notice_category + notice.notice_type
        user_notice.notice_cattype = cattype

        user_notices_to_create.append(user_notice)

    try:
        UserNotices.objects.bulk_create(user_notices_to_create)
    except IntegrityError:
        # MUWM-2016.  This should be rare - 2 processes running at just about
        # exactly the same time.  In that case especially, the bulk create list
        # should be the same.  And if it isn't, big deal?
        pass

    # Add newly created UserNotices into returned list
    notices_with_read_status = notices_with_read_status + notice_dict.values()
    return notices_with_read_status


def _is_tuition_due_notice(notice):
    category = notice.notice_category
    notice_type = notice.notice_type
    if category + "_" + notice_type == "StudentDAD_TuitDue":
        return True
    return False


def get_tuition_due_date():
    tuition_date = None
    notices = get_notices_for_current_user()
    for notice in notices:
        if _is_tuition_due_notice(notice):
            tuition_notice = _store_tuition_notice_date(notice)
            if tuition_notice is not None:
                tuition_date = tuition_notice.date
    if tuition_date is None:
        try:
            stored_tuition = TuitionDate.objects.get(user=get_user_model())
            tuition_date = stored_tuition.date
        except:
            pass
    return tuition_date


def _store_tuition_notice_date(notice):
    for attrib in notice.attributes:
        if attrib.name == "Date":
            defaults = {'date': attrib.get_value()}
            td_get_or_create = TuitionDate.objects.get_or_create
            tuition_date, created = td_get_or_create(user=get_user_model(),
                                                     defaults=defaults)
            if not created:
                tuition_date.date = attrib.get_value()
                tuition_date.save()
            return tuition_date
    return None
