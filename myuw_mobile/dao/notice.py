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
    ("StudentDAD_QtrBegin", "Calendar"),
    ("StudentDAD_QtrEnd", "Calendar"),
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

NOTICE_MAPPING = {
    "UGApplGEN_ThankYouForApplying": {
        "myuw_category": "Admission",
        "location_tags": None,
        "critical": False
    },
    "UGApplGEN_ApplInfoLinks": {
        "myuw_category": "Admission",
        "location_tags": None,
        "critical": False
    },
    "UGApplGEN_AdmWebSites": {
        "myuw_category": "Admission",
        "location_tags": None,
        "critical": False
    },
    "NewStudentCLIST_AdvOrientRegDate": {
        "myuw_category": "Advising",
        "location_tags": None,
        "critical": False
    },
    "NewStudentFOOT_FIUTS": {
        "myuw_category": "Advising",
        "location_tags": None,
        "critical": False
    },
    "StudentGEN_AcctBalance": {
        "myuw_category": "Fees & Finances",
        "location_tags": ["card_finances_tuition_balance", "page_finances_tuition_balance"],
        "critical": False
    },
    "StudentGEN_AcctBalEONote": {
        "myuw_category": "Fees & Finances",
        "location_tags": ["card_finance_PCE_fee_notice", "page_finance_PCE_fee_notice"],
        "critical": False
    },
    "StudentDAD_TuitDue": {
        "myuw_category": "Fees & Finances",
        "location_tags": ["card_finance_tuition_due_date", "page_finance_tuition_due_date", "notice"],
        "critical": True
    },
    "NewStudentGEN_ThankYouRemark": {
        "myuw_category": "Fees & Finances",
        "location_tags": None,
        "critical": False
    },
    "NewStudentGEN_FeesPaid": {
        "myuw_category": "Fees & Finances",
        "location_tags": None,
        "critical": False
    },
    "NewStudentCLIST_FinAid": {
        "myuw_category": "Fees & Finances",
        "location_tags": None,
        "critical": False
    },
    "StudentGEN_DegreeAppl": {
        "myuw_category": "Graduation",
        "location_tags": None,
        "critical": False
    },
    "StudentDAD_Commencement": {
        "myuw_category": "Graduation",
        "location_tags": None,
        "critical": False
    },
    "StudentALR_IntlStuCheckIn": {
        "myuw_category": "Holds",
        "location_tags": ["notice"],
        "critical": True
    },
    "StudentALR_AdminHolds": {
        "myuw_category": "Holds",
        "location_tags": ["reg_trans_hold", "notice"],
        "critical": True
    },
    "StudentALR_SatProgBlock": {
        "myuw_category": "Holds",
        "location_tags": ["ac_prog_hold", "notice"],
        "critical": True
    },
    "StudentDAD_LastDayChgIns": {
        "myuw_category": "Insurance",
        "location_tags": ["notice"],
        "critical": False
    },
    "StudentGEN_FERPA": {
        "myuw_category": "Legal",
        "location_tags": ["notice"],
        "critical": False
    },
    "StudentGEN_IntendedMajors": {
        "myuw_category": None,
        "location_tags": None,
        "critical": False
    },
    "StudentGEN_MajorsMinors": {
        "myuw_category": None,
        "location_tags": None,
        "critical": False
    },
    "NewStudentGEN_StatusSummary": {
        "myuw_category": None,
        "location_tags": None,
        "critical": False
    },
    "NewStudentCLIST_IntendedMajor": {
        "myuw_category": None,
        "location_tags": None,
        "critical": False
    },
    "StudentALR_PreRegNow": {
        "myuw_category": "Registration",
        "location_tags": ["before_reg_ins", "notice"],
        "critical": True
    },
    "StudentDAD_EstPd1RegDate": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "est_reg_date"],
        "critical": False
    },
    "StudentDAD_IntlStuFTRegCutoffDate": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "ISS_reg_cutoff"],
        "critical": False
    },
    "StudentDAD_LastDayRegWOChgFee": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "reg_date_group"],
        "critical": False
    },
    "StudentDAD_LastDayRegChgFee": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "reg_date_group"],
        "critical": False
    },
    "StudentDAD_LastDayDropNoRecord": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "reg_date_group"],
        "critical": False
    },
    "StudentDAD_LastDayAuditOpt": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "reg_date_group"],
        "critical": False
    },
    "StudentDAD_LastDayWOAnnualDrop": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "reg_date_group"],
        "critical": False
    },
    "StudentDAD_LastDayDrop": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "reg_date_group"],
        "critical": False
    },
    "StudentDAD_LastDayAdd": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "reg_date_group"],
        "critical": False
    },
    "StudentDAD_LastDayAnnualDrop": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "reg_date_group"],
        "critical": False
    },
    "StudentDAD_LastDayChgGradeOpt": {
        "myuw_category": "Registration",
        "location_tags": ["notice", "reg_date_group"],
        "critical": False
    },
    "StudentDAD_LastDayWithdraw": {
        "myuw_category": None,
        "location_tags": None,
        "critical": False
    },
    "NewStudentCLIST_IntlStuCheckIn": {
        "myuw_category": "Registration",
        "location_tags": ["reg_info_group"],
        "critical": False
    },
    "NewStudentCLIST_Measles": {
        "myuw_category": "Registration",
        "location_tags": None,
        "critical": False
    },
    "NewStudentFOOT_SummerRegInfo": {
        "myuw_category": "Registration",
        "location_tags": None,
        "critical": False
    },
    "NewStudentFOOT_NextStep": {
        "myuw_category": "Registration",
        "location_tags": None,
        "critical": False
    },
    "StudentDAD_IntlStuRegCutoffDate": {
        "myuw_category": "Visa",
        "location_tags": ["notice"],
        "critical": True
    },
    "StudentGEN_RIAA": {
        "myuw_category": "Legal",
        "location_tags": ["notice"],
        "critical": False
    },
    "StudentDAD_QtrBegin": {
        "myuw_category": None,
        "location_tags": ["notice"],
        "critical": False
    },
    "StudentDAD_QtrEnd": {
        "myuw_category": None,
        "location_tags": ["notice"],
        "critical": False
    }


}

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

def _map_notice(notice):
    key = notice.notice_category + "_" + notice.notice_type
    map_data = NOTICE_MAPPING.get(key, None)
    if map_data is not None:
        notice.custom_category = map_data["myuw_category"]
        notice.is_critical = map_data["critical"]
        notice.location_tags = map_data["location_tags"]