import json
import traceback
from myuw.util.thread import Thread
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
    get_limit_estimate_enrollment_for_section, get_instructor_section
from myuw.dao.term import get_current_quarter
from myuw.dao.term import get_specific_term, is_past, is_future
from myuw.logger.logresp import log_success_response
from myuw.views.rest_dispatch import RESTDispatch
from myuw.dao.exceptions import NotSectionInstructorException

from restclients.sws.term import get_term_before, get_term_after
from restclients.exceptions import DataFailureException


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


def set_course_url(section_data, section):
    canvas_course = get_canvas_course_from_section(section)
    if canvas_course:
        section_data["canvas_url"] = canvas_course.course_url


def load_schedule(request, schedule, summer_term=""):

    json_data = schedule.json_data()

    json_data["summer_term"] = summer_term

    json_data["related_terms"] = _load_related_terms(request)
    json_data["past_term"] = is_past(schedule.term, request)
    json_data["future_term"] = is_future(schedule.term, request)

    colors = get_colors_by_schedule(schedule)

    buildings = get_buildings_by_schedule(schedule)

    # Since the schedule is restclients, and doesn't know
    # about color ids, backfill that data
    section_index = 0
    course_url_threads = []
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

        try:
            t = Thread(target=set_course_url, args=(section_data, section))
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

    if hasattr(schedule, 'section_references'):
        section_references = []
        for section_ref in schedule.section_references:
            section_references.append({
                'term': section_ref.term.json_data(),
                'curriculum_abbr': section_ref.curriculum_abbr,
                'course_number': section_ref.course_number,
                'section_id': section_ref.section_id,
                'url': section_ref.url})

        json_data['section_references'] = section_references

    json_data["is_grad_student"] = is_grad_student()
    return json_data


def _load_related_terms(request):
    current_term = get_current_quarter(request)
    json_data = current_term.json_data()
    terms = [json_data]
    term = current_term
    for i in range(8):
        try:
            term = get_term_before(term)
            json_data = term.json_data()
            terms.insert(0, json_data)
        except DataFailureException as ex:
            if ex.status == 404:
                pass

    term = current_term
    for i in range(2):
        try:
            term = get_term_after(term)
            json_data = term.json_data()
            terms.append(json_data)
        except DataFailureException as ex:
            if ex.status == 404:
                pass
    return terms


class InstScheCurQuar(InstSche):
    """
    Performs actions on resource at /api/v1/instructor_schedule/current/
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


class InstScheQuar(InstSche):
    """
    Performs actions on resource at
    /api/v1/instructor_schedule/<year>,<quarter>(,<summer_term>)?
    """
    def GET(self, request, year, quarter, summer_term=None):
        """
        GET returns 200 with a specific term instructor schedule
        @return course schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        try:
            smr_term = ""
            if summer_term and len(summer_term) > 1:
                smr_term = summer_term.title()

            return self.make_http_resp(timer,
                                       get_specific_term(year, quarter),
                                       request, smr_term)
        except Exception:
            return handle_exception(logger, timer, traceback)


class InstSect(RESTDispatch):
    """
    Performs actions on resource at
    /api/v1/instructor_section/<year>,<quarter>,<curriculum>,
        <course_number>,<course_section>?
    """
    def make_http_resp(self, timer, year, quarter, curriculum, course_number,
                       course_section, request):
        """
        @return instructor schedule data in json format
                status 404: no schedule found (teaching no courses)
        """
        try:
            schedule = get_instructor_section(year, quarter, curriculum,
                                              course_number, course_section)
        except NotSectionInstructorException:
            reason = "Read Access Forbidden to Non Instructor"
            response = HttpResponse(reason)
            response.status_code = 403
            response.reason_phrase = reason
            return response

        resp_data = load_schedule(request, schedule)
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))

    def GET(self, request, year, quarter, curriculum,
            course_number, course_section):
        """
        GET returns 200 with a specific term instructor schedule
        @return course schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        try:
            return self.make_http_resp(timer, year, quarter, curriculum,
                                       course_number, course_section,
                                       request)
        except Exception:
            return handle_exception(logger, timer, traceback)
