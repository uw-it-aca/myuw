"""
This class encapsulates the interactions with 
the SWS notice resource.
"""

import logging
import traceback
from restclients.sws.notice import get_notices_by_regid
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception, log_info
from myuw_mobile.dao.pws import get_regid_of_current_user
from myuw_mobile.models import UserNotices
from myuw_mobile.dao import get_user_model
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)

"""
Categorization of notices into UX defined categories based on the category &
type coming from the notice resource
("[category]_[type]", "[myuw category]")
"""

NOTICE_CATEGORIES = [
    ("StudentDAD_IntlStuRegCutoffDate", "Visa"),
    ("StudentGEN_FERPA", "Me_at_UW"),
    ("StudentGEN_IntendedMajors", "Me_at_UW"),
    ("StudentGEN_MajorsMinors", "Me_at_UW"),
    ("NewStudentGEN_StatusSummary", "Me_at_UW"),
    ("NewStudentCLIST_IntendedMajor", "Me_at_UW"),
    ("NewStudentCLIST_AdvOrientRegDate", "Advising"),
    ("NewStudentFOOT_FIUTS", "Advising"),
    ("StudentALR_PreRegNow", "Registration"),
    ("StudentDAD_EstPd1RegDate", "Registration"),
    ("StudentDAD_IntlStuFTRegCutoffDate", "Registration"),
    ("StudentDAD_LastDayRegWOChgFee", "Registration"),
    ("StudentDAD_LastDayRegChgFee", "Registration"),
    ("StudentDAD_LastDayDropNoRecord", "Registration"),
    ("StudentDAD_LastDayAuditOpt", "Registration"),
    ("StudentDAD_LastDayWOAnnualDrop", "Registration"),
    ("StudentDAD_LastDayDrop", "Registration"),
    ("StudentDAD_LastDayAdd", "Registration"),
    ("StudentDAD_LastDayAnnualDrop", "Registration"),
    ("StudentDAD_LastDayChgGradeOpt", "Registration"),
    ("StudentDAD_LastDayWithdraw", "Registration"),
    ("NewStudentCLIST_IntlStuCheckIn", "Registration"),
    ("NewStudentCLIST_Measles", "Registration"),
    ("NewStudentFOOT_SummerRegInfo", "Registration"),
    ("NewStudentFOOT_NextStep", "Registration"),
    ("UGApplGEN_ThankYouForApplying", "Admission"),
    ("UGApplGEN_ApplInfoLinks", "Admission"),
    ("UGApplGEN_AdmWebSites", "Admission"),
    ("StudentALR_IntlStuCheckIn", "Holds"),
    ("StudentALR_AdminHolds", "Holds"),
    ("StudentALR_SatProgBlock", "Holds"),
    ("StudentDAD_LastDayChgIns", "Insurance"),
    ("StudentGEN_DegreeAppl", "Graduation"),
    ("StudentDAD_Commencement", "Graduation"),
    ("StudentGEN_AcctBalance", "Finance"),
    ("StudentGEN_AcctBalEONote", "Finance"),
    ("StudentDAD_TuitDue", "Finance"),
    ("NewStudentGEN_ThankYouRemark", "Finance"),
    ("NewStudentGEN_FeesPaid", "Finance"),
    ("NewStudentCLIST_FinAid", "Finance")
]

UNKNOWN_CATEGORY_NAME = "Uncategorized"


def _get_notices_by_regid(user_regid):
    """
    returns SWS notices for a given regid with
    myuw specific categories
    """

    if user_regid is None:
        return None

    timer = Timer()

    try:
        notices = get_notices_by_regid(user_regid)
        if notices is not None:
            return _categorize_notices(notices)
    except Exception:
        log_exception(logger,
                      'Notice.get_notices',
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                      'Notice.get_notices',
                      timer)
    return None


def get_notices_for_current_user():
    notices = _get_notices_by_regid(get_regid_of_current_user())
    if notices is None:
        return []
    for notice in notices:
        user_notice = _get_user_notice(notice)
        notice.id_hash = user_notice.notice_hash
        notice.is_read = user_notice.is_read

    return notices


def _get_user_notice(notice):
    notice_hash = UserNotices().generate_hash(notice)
    user_notice = None
    try:
        user_notice = UserNotices.objects.get(notice_hash=notice_hash)
    except ObjectDoesNotExist:
        user = get_user_model()
        user_notice = UserNotices()
        user_notice.notice_hash = notice_hash
        user_notice.user = user
        user_notice.save()
    notice.id_hash = user_notice.notice_hash
    return user_notice

def _categorize_notices(notices):
    for notice in notices:
        notice.custom_category = _get_notice_category(notice)
    return notices


def _get_notice_category(notice):
    key = notice.notice_category + "_" + notice.notice_type
    key_list, category_list = zip(*NOTICE_CATEGORIES)
    try:
        index = key_list.index(key)
        return category_list[index]
    except ValueError:
        log_info(logger, "No category found for %s" % key)
        return UNKNOWN_CATEGORY_NAME
