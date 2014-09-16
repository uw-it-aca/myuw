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
from myuw_mobile.models import UserNotices, TuitionDate
from myuw_mobile.dao import get_user_model
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)

"""
Categorization of notices into UX defined categories, location tags, and
criticality based on the category & type coming from the notice resource
"""


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
          "NewStudentFOOT_FIUTS": {
              "myuw_category": "Advising? Orientation?",
              "location_tags": None,
              "critical": False
          },
          "StudentGEN_AcctBalance": {
              "myuw_category": "Fees & Finances",
              "location_tags": ['tuition_balance', 'finance_card'],
              "critical": False
          },
          "StudentGEN_AcctBalEONote": {
              "myuw_category": "Fees & Finances",
              "location_tags": ['pce_tuition_dup', 'finance_card'],
              "critical": False
          },
          "StudentDAD_TuitDue": {
              "myuw_category": "Fees & Finances",
              "location_tags": ['tuition_due_date', 'finance_card', 'notice_date_sort'],
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
              "location_tags": ['finance_card_finaid'],
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
              "location_tags": ['notices_holds', 'reg_card_holds'],
              "critical": True
          },
          "StudentALR_AdminHolds": {
              "myuw_category": "Holds",
              "location_tags": ['notices_holds', 'reg_card_holds'],
              "critical": True
          },
          "StudentALR_SatProgBlock": {
              "myuw_category": "Holds",
              "location_tags": ['notices_holds', 'reg_card_holds'],
              "critical": True
          },
          "StudentDAD_LastDayChgIns": {
              "myuw_category": "Insurance",
              "location_tags": None,
              "critical": False
          },
          "StudentGEN_FERPA": {
              "myuw_category": "Legal",
              "location_tags": ['notices_legal'],
              "critical": False
          },
          "StudentGEN_IntendedMajors": {
              "myuw_category": "not a notice",
              "location_tags": None,
              "critical": False
          },
          "StudentGEN_MajorsMinors": {
              "myuw_category": "not a notice",
              "location_tags": None,
              "critical": False
          },
          "NewStudentGEN_StatusSummary": {
              "myuw_category": "not a notice",
              "location_tags": None,
              "critical": False
          },
          "NewStudentCLIST_IntendedMajor": {
              "myuw_category": "not a notice",
              "location_tags": None,
              "critical": False
          },
          "StudentALR_PreRegNow": {
              "myuw_category": "Registration",
              "location_tags": ['reg_card_messages'],
              "critical": True
          },
          "StudentDAD_EstPd1RegDate": {
              "myuw_category": "Registration",
              "location_tags": ['est_reg_date', 'notices_date_sort'],
              "critical": True
          },
          "StudentDAD_IntlStuFTRegCutoffDate": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": True
          },
          "StudentDAD_LastDayRegWOChgFee": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": False
          },
          "StudentDAD_LastDayRegChgFee": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": False
          },
          "StudentDAD_LastDayDropNoRecord": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": False
          },
          "StudentDAD_LastDayAuditOpt": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": False
          },
          "StudentDAD_LastDayWOAnnualDrop": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": False
          },
          "StudentDAD_LastDayDrop": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": False
          },
          "StudentDAD_LastDayAdd": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": False
          },
          "StudentDAD_LastDayAnnualDrop": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": False
          },
          "StudentDAD_LastDayChgGradeOpt": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": False
          },
          "StudentDAD_LastDayWithdraw": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort'],
              "critical": False
          },
          "NewStudentCLIST_IntlStuCheckIn": {
              "myuw_category": "Registration",
              "location_tags": ['notices_holds'],
              "critical": False
          },
          "NewStudentCLIST_AdvOrientRegDate": {
              "myuw_category": "Registration",
              "location_tags": ['notices_date_sort', 'reg_card_messages'],
              "critical": False
          },
          "NewStudentCLIST_Measles": {
              "myuw_category": "Registration",
              "location_tags": ['?'],
              "critical": False
          },
          "NewStudentFOOT_SummerRegInfo": {
              "myuw_category": "Registration",
              "location_tags": ['reg_card_messages'],
              "critical": False
          },
          "NewStudentFOOT_NextStep": {
              "myuw_category": "Registration? Advising? ",
              "location_tags": ['?'],
              "critical": False
          },
          "StudentDAD_IntlStuRegCutoffDate": {
              "myuw_category": "Visa",
              "location_tags": None,
              "critical": True
          },
          "StudentGEN_RIAA": {
              "myuw_category": "Legal",
              "location_tags": ['notices_legal'],
              "critical": False
          },
          "StudentDAD_QtrBegin": {
              "myuw_category": "",
              "location_tags": ['quarter_begins'],
              "critical": False
          },
          "StudentDAD_QtrEnd": {
              "myuw_category": "Quarter Ends",
              "location_tags": ['quarter_ends'],
              "critical": False
          },

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

def mark_notices_read_for_current_user(notice_hashes):
    user = get_user_model()
    UserNotices().mark_notices_read(notice_hashes, user)

def get_notices_for_current_user():
    notices = _get_notices_by_regid(get_regid_of_current_user())
    if notices is None:
        return []
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
    user_notices = UserNotices.objects.filter(user=user, notice_hash__in=notice_dict.keys())
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
        user_notices_to_create.append(user_notice)
    UserNotices.objects.bulk_create(user_notices_to_create)

    # Add newly created UserNotices into returned list
    notices_with_read_status = notices_with_read_status + notice_dict.values()
    return notices_with_read_status

def _categorize_notices(notices):
    for notice in notices:
        _map_notice(notice)
    notices[:] = [notice for notice in notices if notice.custom_category != "not a notice"]
    return notices

def _map_notice(notice):
    key = notice.notice_category + "_" + notice.notice_type
    map_data = NOTICE_MAPPING.get(key, None)
    if map_data is not None:
        if len(map_data["myuw_category"]) == 0:
            notice.custom_category = UNKNOWN_CATEGORY_NAME
        else:
            notice.custom_category = map_data["myuw_category"]
        notice.is_critical = map_data["critical"]
        notice.location_tags = map_data["location_tags"]
    else:
        notice.custom_category = UNKNOWN_CATEGORY_NAME
        notice.is_critical = False
        notice.location_tags = None

def get_tuition_due_date():
    tuition_date = None
    notices = get_notices_for_current_user()
    for notice in notices:
        if notice.notice_category + "_" + notice.notice_type == "StudentDAD_TuitDue":
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
            tuition_date, created = TuitionDate.objects.get_or_create(user=get_user_model(),
                                                                      defaults={'date': attrib.get_value()})
            if not created:
                tuition_date.date = attrib.get_value()
                tuition_date.save()
            return tuition_date
    return None
