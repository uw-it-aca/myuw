import json
import logging
from myuw.util.thread import Thread
from django.http import HttpResponse
from operator import itemgetter
from uw_sws.section import is_valid_sln
from myuw.dao.building import get_buildings_by_schedule
from myuw.dao.canvas import (get_canvas_active_enrollments,
                             canvas_course_is_available)
from myuw.dao.course_color import get_colors_by_schedule
from myuw.dao.enrollment import (get_enrollment_for_term,
                                 is_ended)
from myuw.dao.gws import is_grad_student
from myuw.dao.library import get_subject_guide_by_section
from myuw.dao.schedule import get_schedule_by_term,\
    filter_schedule_sections_by_summer_term
from myuw.dao.registered_term import get_current_summer_term_in_schedule
from myuw.logger.logresp import (log_data_not_found_response,
                                 log_success_response, log_msg)
from myuw.views.rest_dispatch import RESTDispatch
from myuw.views.error import data_not_found
from myuw.views import prefetch_resources


logger = logging.getLogger(__name__)


class StudClasSche(RESTDispatch):
    def run(self, request, *args, **kwargs):
        prefetch_resources(request,
                           prefetch_enrollment=True,
                           prefetch_library=True,
                           prefetch_person=True,
                           prefetch_canvas=True)
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

    try:
        enrollment = get_enrollment_for_term(schedule.term)
        enrolled_off_term_sections = enrollment.off_term_sections
    except Exception as ex:
        logger.error("find enrolled off term sections: %s", ex)
        enrolled_off_term_sections = {}
        pass

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

        if section.is_early_fall_start():
            section_data["cc_display_dates"] = True
            section_data["early_fall_start"] = True
            json_data["has_early_fall_start"] = True
            section_data["is_ended"] = is_ended(request, section.end_date)
        else:
            if len(enrolled_off_term_sections) > 0 and\
                    section.section_label() in enrolled_off_term_sections:
                # print enrolled_off_term_sections.get(
                #    section.section_label()).json_data()
                enrolled_sect = enrolled_off_term_sections.get(
                    section.section_label())
                section_data["cc_display_dates"] = True
                section_data["start_date"] = str(enrolled_sect.start_date)
                section_data["end_date"] = str(enrolled_sect.end_date)
                section_data["is_ended"] = is_ended(request,
                                                    enrolled_sect.end_date)

        # if section.is_primary_section:
        if not is_valid_sln(section.sln):
            section_data["sln"] = 0
        else:
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
