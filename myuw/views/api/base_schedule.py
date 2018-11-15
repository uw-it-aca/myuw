import logging
import traceback
from myuw.util.thread import Thread
from operator import itemgetter
from restclients_core.exceptions import InvalidNetID
from myuw.dao.building import get_buildings_by_schedule
from myuw.dao.canvas import (get_canvas_active_enrollments,
                             canvas_course_is_available)
from myuw.dao.enrollment import get_enrollment_for_term, is_ended
from myuw.dao.library import get_subject_guide_by_section
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.schedule import (
    get_schedule_by_term, filter_schedule_sections_by_summer_term)
from myuw.dao.registered_term import get_current_summer_term_in_schedule
from myuw.logger.logresp import (
    log_data_not_found_response, log_api_call, log_exception)
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found, unknown_uwnetid
from myuw.views import prefetch_resources

logger = logging.getLogger(__name__)


class StudClasSche(ProtectedAPI):

    def dispatch(self, request, *args, **kwargs):
        try:
            person = get_person_of_current_user(request)
        except InvalidNetID:
            return unknown_uwnetid()

        try:
            prefetch_resources(request,
                               prefetch_enrollment=True,
                               prefetch_library=True,
                               prefetch_canvas=True)
            return super(StudClasSche, self).dispatch(request, *args, **kwargs)
        except Exception as ex:
            log_exception(logger, 'StudClasSche.dispatch',
                          traceback.format_exc(chain=False))

    def make_http_resp(self, timer, term, request, summer_term=None):
        """
        @return class schedule data in json format
                status 404: no schedule found (not registered)
        """
        schedule = get_schedule_by_term(request, term)

        if summer_term is None:
            summer_term = get_current_summer_term_in_schedule(schedule,
                                                              request)

        filter_schedule_sections_by_summer_term(schedule, summer_term)
        if len(schedule.sections) == 0:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        resp_data = load_schedule(request, schedule, summer_term)
        log_api_call(timer, request,
                     "Get Student Schedule {},{}".format(term.year,
                                                         term.quarter))
        return self.json_response(resp_data)


def set_course_url(section_data, enrollment):
    if canvas_course_is_available(enrollment.course_id):
        section_data["canvas_url"] = enrollment.course_url


def load_schedule(request, schedule, summer_term=""):
    json_data = schedule.json_data()

    json_data["summer_term"] = summer_term

    buildings = get_buildings_by_schedule(schedule)

    try:
        enrollment = get_enrollment_for_term(request, schedule.term)
        pce_sections = enrollment.unf_pce_courses
    except Exception as ex:
        logger.error("find enrolled off term sections ({} {}): {}".format(
                     schedule.term.quarter, schedule.term.year, str(ex)))
        pce_sections = {}
        pass

    canvas_enrollments = {}
    try:
        canvas_enrollments = get_canvas_active_enrollments(request)
    except Exception:
        log_exception(logger, 'load_schedule',
                      traceback.format_exc(chain=False))
        pass

    section_index = 0
    course_url_threads = []
    json_data["has_eos_dates"] = False
    for section in schedule.sections:
        section_data = json_data["sections"][section_index]
        section_index += 1

        section_data["color_id"] = section.color_id

        if not section_data["section_type"]:
            if len(section.meetings) > 0:
                section_data["section_type"] = section.meetings[0].meeting_type

        if section.is_early_fall_start():
            section_data["cc_display_dates"] = True
            section_data["early_fall_start"] = True
            json_data["has_early_fall_start"] = True
            section_data["is_ended"] = is_ended(request, section.end_date)
        else:
            if len(pce_sections) > 0 and\
                    section.section_label() in pce_sections:
                pce_course = pce_sections.get(section.section_label())
                section_data["on_standby"] = pce_course.standby()
                group_independent_start = irregular_start_end(
                    schedule.term, pce_course, section.summer_term)
                if group_independent_start:
                    section_data["cc_display_dates"] = True
                    section_data["start_date"] = str(pce_course.start_date)
                    section_data["end_date"] = str(pce_course.end_date)
                    section_data["is_ended"] = is_ended(request,
                                                        pce_course.end_date)

        # if section.is_primary_section:
        if section.sln:
            try:
                section_data["lib_subj_guide"] =\
                    get_subject_guide_by_section(section)
            except Exception:
                log_exception(logger, 'load_schedule',
                              traceback.format_exc(chain=False))
                pass

        try:
            enrollment = canvas_enrollments[section.section_label()]
            t = Thread(target=set_course_url, args=(section_data, enrollment))
            course_url_threads.append(t)
            t.start()
        except KeyError:
            pass

        # MUWM-596
        if section.final_exam and section.final_exam.building:
            building = buildings[section.final_exam.building]
            if building:
                section_data["final_exam"]["longitude"] = building.longitude
                section_data["final_exam"]["latitude"] = building.latitude
                section_data["final_exam"]["building_name"] = building.name

        # Also backfill the meeting building data
        section_data["has_eos_dates"] = False
        meeting_index = 0
        for meeting in section.meetings:
            mdata = section_data["meetings"][meeting_index]

            if meeting.eos_start_date is not None:
                if not section_data["has_eos_dates"]:
                    section_data["has_eos_dates"] = True

                mdata["start_end_same"] = False
                if mdata["eos_start_date"] == mdata["eos_end_date"]:
                    mdata["start_end_same"] = True
            try:
                if not mdata["building_tbd"] and len(mdata["building"]):
                    building = buildings.get(mdata["building"])
                    if building is not None:
                        mdata["latitude"] = building.latitude
                        mdata["longitude"] = building.longitude
                        mdata["building_name"] = building.name

                for instructor in mdata["instructors"]:
                    if (len(instructor["email_addresses"]) == 0 and
                            len(instructor["phones"]) == 0 and
                            len(instructor["voice_mails"]) == 0 and
                            len(instructor["faxes"]) == 0 and
                            len(instructor["touch_dials"]) == 0 and
                            len(instructor["addresses"]) == 0):
                        instructor["whitepages_publish"] = False
                meeting_index += 1
            except IndexError as ex:
                pass
        if section_data["has_eos_dates"]:
            if not json_data["has_eos_dates"]:
                json_data["has_eos_dates"] = True
            section_data["meetings"] = sort_pce_section_meetings(
                section_data["meetings"])

    for t in course_url_threads:
        t.join()

    # MUWM-443
    json_data["sections"] = sorted(json_data["sections"],
                                   key=itemgetter('curriculum_abbr',
                                                  'course_number',
                                                  'section_id',
                                                  ))
    # add section index
    index = 0
    for section in json_data["sections"]:
        section["index"] = index
        index = index + 1

    return json_data


def irregular_start_end(term, pce_course_data, summer_term):
    if len(summer_term) and summer_term.lower() == "a-term":
        return (term.first_day_quarter != pce_course_data.start_date or
                term.aterm_last_date != pce_course_data.end_date)
    if len(summer_term) and summer_term.lower() == "b-term":
        return (term.bterm_first_date != pce_course_data.start_date or
                term.last_final_exam_date != pce_course_data.end_date)
    return (term.first_day_quarter != pce_course_data.start_date or
            term.last_final_exam_date != pce_course_data.end_date)


def sort_pce_section_meetings(section_meetings_json_data):
    """
    Sort meeting by eos_start_date
    """
    ret_list = sorted(section_meetings_json_data,
                      key=itemgetter('eos_start_date'))
    # add section index
    index = 0
    for meeting in ret_list:
        meeting["index"] = index
        index = index + 1

    return ret_list
