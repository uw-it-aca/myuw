# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import traceback
from operator import itemgetter
from restclients_core.exceptions import InvalidNetID
from myuw.dao.building import get_buildings_by_schedule
from myuw.dao.canvas import (
    get_canvas_active_enrollments, set_section_canvas_course_urls)
from myuw.dao.enrollment import get_enrollment_for_term, is_ended
from myuw.dao.library import get_subject_guide_by_section
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.registration import get_schedule_by_term
# from myuw.dao.schedule import filter_schedule_sections_by_summer_term
# from myuw.dao.registered_term import get_current_summer_term_in_schedule
from myuw.logger.timer import Timer
from myuw.logger.logresp import (
    log_data_not_found_response, log_api_call, log_exception)
from myuw.views.api import ProtectedAPI
from myuw.views.error import data_not_found, unknown_uwnetid, handle_exception
from myuw.views import prefetch_resources

logger = logging.getLogger(__name__)


class StudClasSche(ProtectedAPI):

    def dispatch(self, request, *args, **kwargs):
        timer = Timer()
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
        except Exception:
            handle_exception(logger, timer, traceback)

    def make_http_resp(self, timer, term, request, summer_term=None):
        """
        @return class schedule data in json format
                status 404: no schedule found (not registered)
        """
        schedule = get_schedule_by_term(
            request, term=term, summer_term=summer_term)

        if len(schedule.sections) == 0:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        resp_data = load_schedule(request, schedule)
        log_api_call(timer, request,
                     "Get Student Schedule {},{}".format(term.year,
                                                         term.quarter))
        return self.json_response(resp_data)


def load_schedule(request, schedule):
    json_data = schedule.json_data()
    if schedule.term.is_summer_quarter():
        json_data["summer_term"] = schedule.summer_term
    buildings = get_buildings_by_schedule(schedule)
    if len(schedule.sections):
        try:
            set_section_canvas_course_urls(
                get_canvas_active_enrollments(request), schedule, request)
        except Exception:
            log_exception(logger, 'get_canvas_active_enrollments', traceback)
            pass

    section_index = 0
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
            if irregular_start_end(schedule.term, section):
                section_data["cc_display_dates"] = True
                section_data["is_ended"] = is_ended(request, section.end_date)
            section_data["on_standby"] = (
                section.registration.is_standby_status())

        try:
            section_data["canvas_url"] = section.canvas_course_url
        except Exception:
            pass

        # if section.is_primary_section:
        if section.sln:
            try:
                section_data["lib_subj_guide"] =\
                    get_subject_guide_by_section(section)
            except Exception:
                log_exception(logger,
                              'get_subject_guide_by_section', traceback)
                pass

        if section.final_exam:
            final = section_data["final_exam"]
            # MUWM-4728
            final["is_remote"] = section.is_remote

            # MUWM-596
            if section.final_exam.building:
                building = buildings[section.final_exam.building]
                if building:
                    final["longitude"] = building.longitude
                    final["latitude"] = building.latitude
                    final["building_name"] = building.name

        # Also backfill the meeting building data
        section_data["has_eos_dates"] = False
        meeting_index = 0
        for meeting in section.meetings:
            mdata = section_data["meetings"][meeting_index]

            # MUWM-4728
            mdata["is_remote"] = section.is_remote

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


def irregular_start_end(term, section):
    if section.start_date is None or section.end_date is None:
        return False
    if section.is_summer_a_term():
        return (term.first_day_quarter != section.start_date or
                term.aterm_last_date != section.end_date)
    if section.is_summer_b_term():
        return (term.bterm_first_date != section.start_date or
                term.last_day_instruction != section.end_date)
    return (term.first_day_quarter != section.start_date or
            term.last_final_exam_date != section.end_date)  # MUWM-4863


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
