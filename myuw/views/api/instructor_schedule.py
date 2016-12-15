import json
import traceback
from myuw.dao.term import get_current_quarter, get_next_quarter
from myuw.logger.timer import Timer
from myuw.views.rest_dispatch import handle_exception

import logging
from django.http import HttpResponse
from operator import itemgetter
from myuw.dao.building import get_buildings_by_schedule
from myuw.dao.canvas import get_canvas_course_from_section
from myuw.dao.course_color import get_colors_by_schedule
from myuw.dao.gws import is_grad_student
from myuw.dao.library import get_subject_guide_by_section
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term,\
    get_limit_estimate_enrollment_for_section
from myuw.dao.registered_term import get_current_summer_term_in_schedule
from myuw.dao.term import get_comparison_date
from myuw.logger.logresp import log_data_not_found_response,\
    log_success_response, log_msg
from myuw.views.rest_dispatch import RESTDispatch, data_not_found
from restclients.sws.term import get_term_before, get_term_after


logger = logging.getLogger(__name__)
EARLY_FALL_START = "EARLY FALL START"


class InstSche(RESTDispatch):

    def make_http_resp(self, timer, term, request, summer_term=None):
        """
        @return instructor schedule data in json format
                status 404: no schedule found (teaching no courses)
        """
        schedule = get_instructor_schedule_by_term(term)
        resp_data = load_schedule(request, schedule)
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))


def load_schedule(request, schedule, summer_term=""):

    json_data = schedule.json_data()

    json_data["summer_term"] = summer_term

    colors = get_colors_by_schedule(schedule)

    buildings = get_buildings_by_schedule(schedule)

    # Since the schedule is restclients, and doesn't know
    # about color ids, backfill that data
    section_index = 0
    for section in schedule.sections:
        section_data = json_data["sections"][section_index]
        color = colors[section.section_label()]
        section_data["color_id"] = color
        section_index += 1

        if EARLY_FALL_START == section.institute_name:
            section_data["early_fall_start"] = True
            json_data["has_early_fall_start"] = True
        # if section.is_primary_section:
        try:
            section_data["lib_subj_guide"] =\
                get_subject_guide_by_section(section)
        except Exception as ex:
            logger.error(ex)
            pass

        if not hasattr(section, 'limit_estimate_enrollment'):
            section_data['limit_estimate_enrollment'] =\
                get_limit_estimate_enrollment_for_section(section)

        section_data['grade_submission_delegates'] = []
        for delegate in section.grade_submission_delegates:
            section_data['grade_submission_delegates'].append(
                {
                    'person': delegate.person.json_data(),
                    'level': delegate.delegate_level
                })

        canvas_course = get_canvas_course_from_section(section)
        if canvas_course:
            section_data["canvas_url"] = canvas_course.course_url
            section_data["canvas_name"] = canvas_course.name

        # MUWM-596
        if section.final_exam and section.final_exam.building:
            building = buildings[section.final_exam.building]
            if building:
                section_data["final_exam"]["longitude"] = building.longitude
                section_data["final_exam"]["latitude"] = building.latitude
                section_data["final_exam"]["building_name"] = building.name

        # Also backfill the meeting building data
        meeting_index = 0
        for meeting in section.meetings:
            try:
                mdata = section_data["meetings"][meeting_index]
                if not mdata["building_tbd"]:
                    building = buildings[mdata["building"]]
                    if building is not None:
                        mdata["latitude"] = building.latitude
                        mdata["longitude"] = building.longitude
                        mdata["building_name"] = building.name

                for instructor in mdata["instructors"]:
                    if (
                            not instructor["email1"] and
                            not instructor["email2"] and
                            not instructor["phone1"] and
                            not instructor["phone2"] and
                            not instructor["voicemail"] and
                            not instructor["fax"] and
                            not instructor["touchdial"] and
                            not instructor["address1"] and
                            not instructor["address2"]
                            ):
                        instructor["whitepages_publish"] = False
                meeting_index += 1
            except IndexError as ex:
                pass

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

    json_data["is_grad_student"] = is_grad_student()
    return json_data


class InstScheCurQuar(InstSche):
    """
    Performs actions on resource at /api/v1/instructor/schedule/current/.
    """

    def GET(self, request):
        """
        GET returns 200 with the current quarter course section schedule
        @return class schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        try:
            return self.make_http_resp(timer,
                                       get_current_quarter(request),
                                       request)
        except Exception:
            return handle_exception(logger, timer, traceback)


class InstScheFutuQuar(InstSche):
    """
    Performs actions on resource at /api/v1/instructor/schedule/next/.
    """

    def GET(self, request):
        """
        GET returns 200 with a future quarter course section schedule
        Integer "offset" parameter sets how many quarters forward (default: 1)
        @return class schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        term = get_current_quarter(request)
        offset = int(request.GET.get('offset', 1))
        for index in range(offset):
            term = get_term_after(term)
        try:
            return self.make_http_resp(timer,
                                       term,
                                       request)
        except Exception:
            return handle_exception(logger, timer, traceback)


class InstSchePastQuar(InstSche):
    """
    Performs actions on resource at /api/v1/instructor/schedule/previous/.
    """

    def GET(self, request):
        """
        GET returns 200 with a past quarter course section schedule
        Integer "offset" parameter sets how many quarters past (default: 1)
        @return class schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        term = get_current_quarter(request)
        offset = int(request.GET.get('offset', 1))
        for index in range(offset):
            term = get_term_before(term)
        try:
            return self.make_http_resp(timer,
                                       term,
                                       request)
        except Exception:
            return handle_exception(logger, timer, traceback)
