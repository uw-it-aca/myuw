import json
import logging
from django.http import HttpResponse
from operator import itemgetter
from myuw.dao.building import get_buildings_by_schedule
from myuw.dao.canvas import get_canvas_enrolled_courses,\
    get_indexed_by_decrosslisted
from myuw.dao.course_color import get_colors_by_schedule
from myuw.dao.gws import is_grad_student
from myuw.dao.library import get_subject_guide_by_section
from myuw.dao.schedule import get_schedule_by_term,\
    filter_schedule_sections_by_summer_term
from myuw.dao.registered_term import get_current_summer_term_in_schedule
from myuw.dao.term import get_comparison_date
from myuw.logger.logresp import log_data_not_found_response,\
    log_success_response, log_msg
from myuw.views.rest_dispatch import RESTDispatch, data_not_found


logger = logging.getLogger(__name__)


class StudClasSche(RESTDispatch):

    def make_http_resp(self, timer, term, request, summer_term=None):
        """
        @return class schedule data in json format
                status 404: no schedule found (not registered)
        """
        schedule = get_schedule_by_term(term)

        if summer_term is None:
            summer_term = get_current_summer_term_in_schedule(schedule,
                                                              request)

        filter_schedule_sections_by_summer_term(schedule, summer_term)
        if len(schedule.sections) == 0:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        resp_data = load_schedule(request, schedule, summer_term)
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))


def load_schedule(request, schedule, summer_term=""):

    json_data = schedule.json_data()

    json_data["summer_term"] = summer_term

    colors = get_colors_by_schedule(schedule)

    buildings = get_buildings_by_schedule(schedule)

    canvas_data_by_course_id = []
    try:
        canvas_data_by_course_id = get_indexed_by_decrosslisted(
            get_canvas_enrolled_courses(), schedule.sections)
    except Exception as ex:
        logger.error(ex)
        pass
    # Since the schedule is restclients, and doesn't know
    # about color ids, backfill that data
    section_index = 0
    for section in schedule.sections:
        section_data = json_data["sections"][section_index]
        color = colors[section.section_label()]
        section_data["color_id"] = color
        section_index += 1
        # if section.is_primary_section:
        try:
            section_data["lib_subj_guide"] =\
                get_subject_guide_by_section(section)
        except Exception as ex:
            logger.error(ex)
            pass

        if section.section_label() in canvas_data_by_course_id:
            enrollment = canvas_data_by_course_id[section.section_label()]
            # canvas_grade = enrollment.final_grade
            # section_data["canvas_grade"] = canvas_grade
            canvas_course = enrollment.course
            if not canvas_course.is_unpublished():
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
