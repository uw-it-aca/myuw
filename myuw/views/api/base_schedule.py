import json
import logging
from threading import Thread
from django.http import HttpResponse
from operator import itemgetter
from myuw.dao.building import get_buildings_by_schedule
from myuw.dao.canvas import (get_canvas_active_enrollments,
                             canvas_course_is_available,
                             canvas_prefetch)
from myuw.dao.affiliation import affiliation_prefetch
from myuw.dao.course_color import get_colors_by_schedule
from myuw.dao.gws import is_grad_student
from myuw.dao.pws import person_prefetch
from myuw.dao.library import (get_subject_guide_by_section,
                              library_resource_prefetch)
from myuw.dao.schedule import get_schedule_by_term,\
    filter_schedule_sections_by_summer_term
from myuw.dao.registered_term import get_current_summer_term_in_schedule
from myuw.dao.term import get_comparison_date, current_terms_prefetch
from myuw.logger.logresp import (log_data_not_found_response,
                                 log_success_response, log_msg)
from myuw.views.rest_dispatch import RESTDispatch, data_not_found
from myuw.views import prefetch


logger = logging.getLogger(__name__)
EARLY_FALL_START = "EARLY FALL START"


class StudClasSche(RESTDispatch):
    def run(self, request, *args, **kwargs):
        prefetch_schedule_resources(request)
        return super(StudClasSche, self).run(request, *args, **kwargs)

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
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))


def set_course_url(section_data, enrollment):
    if canvas_course_is_available(enrollment.course_id):
        section_data["canvas_url"] = enrollment.course_url


def load_schedule(request, schedule, summer_term=""):

    json_data = schedule.json_data()

    json_data["summer_term"] = summer_term

    colors = get_colors_by_schedule(schedule)

    buildings = get_buildings_by_schedule(schedule)

    canvas_enrollments = {}
    try:
        canvas_enrollments = get_canvas_active_enrollments()
    except Exception as ex:
        logger.error(ex)
        pass

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

    json_data["is_grad_student"] = is_grad_student()
    return json_data


def prefetch_schedule_resources(request):
    prefetch_methods = []
    prefetch_methods.extend(current_terms_prefetch(request))
    prefetch_methods.extend(library_resource_prefetch())
    prefetch_methods.extend(affiliation_prefetch())
    prefetch_methods.extend(person_prefetch())
    prefetch_methods.extend(canvas_prefetch())

    prefetch(request, prefetch_methods)
