# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
import logging
import traceback
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from myuw.dao import coda, id_photo_token
from myuw.views.error import (
    handle_exception, not_instructor_error)
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.dao.instructor_schedule import (
    get_instructor_section, check_section_instructor)
from myuw.dao.term import is_future
from myuw.logger.logresp import log_api_call
from myuw.logger.timer import Timer
from myuw.util.thread import Thread
from myuw.views.api import OpenAPI
from myuw.views.api.instructor_schedule import (
    load_schedule, _set_current)

logger = logging.getLogger(__name__)
withdrew_grade_pattern = re.compile(r'^W')


def is_registration_to_exclude(registration):
    return (registration.is_withdrew() or
            registration.is_pending_status() or
            registration.is_dropped_status())


def photo_url(uwregid, token):
    return reverse('photo', kwargs={'uwregid': uwregid, 'token': token})


class OpenInstSectionDetails(OpenAPI):
    """
    Performs actions on resource at
    /api/v1/instructor_section/<year>,<quarter>,<curriculum>,
        <course_number>,<course_section>?
    """

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with a specific term instructor schedule
        @return course schedule data in json format
                status 400: invalid section_id
                status 403: not authorized to view section details
                status 404: no schedule found (not registered)
                status 543: data error
        """
        timer = Timer()
        section_id = kwargs.get('section_id')
        try:
            return self.make_http_resp(timer, request, section_id)
        except Exception as ex:
            return handle_exception(logger, timer, traceback)

    def make_http_resp(self, timer, request, section_id):
        """
        @return instructor schedule data in json format
            status 404: no schedule found (teaching no courses)
        """
        self.processed_primary = False
        schedule = get_instructor_section(request,
                                          section_id,
                                          include_registrations=True,
                                          include_linked_sections=True)
        # with the student registration and secondary section data

        try:
            self.is_authorized_for_section(request, schedule)
        except NotSectionInstructorException:
            return not_instructor_error()

        self.term = schedule.term
        resp_data = load_schedule(request, schedule, schedule.summer_term,
                                  section_callback=self.per_section_data)

        _set_current(self.term, request, resp_data)
        # Concurrently fetch section data and ICD data
        threads = []
        t = Thread(target=self.add_linked_section_data,
                   args=(resp_data,))
        threads.append(t)
        t.start()

        if not is_future(self.term, request):
            for section in resp_data['sections']:
                _set_current(self.term, request, section)

                t = Thread(target=coda.get_classlist_details,
                           args=(section['section_label'], section,))
                threads.append(t)
                t.start()

        for thread in threads:
            thread.join()

        self.add_linked_section_data(resp_data)
        log_api_call(timer, request,
                     f"Get Instructor Section Details for {section_id}")

        return self.json_response(resp_data)

    def is_authorized_for_section(self, request, schedule):
        raise NotSectionInstructorException()

    def add_linked_section_data(self, resp_data):
        sections_for_user = {}  # {regid: [section_id,]}
        has_linked_sections = False

        # if having linked sections
        for section in resp_data["sections"][1:]:
            section_id = section["section_id"]
            for regid in section["registrations"]:
                if regid not in sections_for_user:
                    sections_for_user[regid] = []
                sections_for_user[regid].append(section_id)

        for registration in resp_data["sections"][0]["registrations"]:
            registration["linked_sections"] = ""
            regid = registration["regid"]
            if sections_for_user.get(regid):
                registration["linked_sections"] = " ".join(
                    sections_for_user[regid])
                has_linked_sections = True
        resp_data["sections"][0]['has_linked_sections'] =\
            has_linked_sections

    def per_section_data(self, section, section_data):
        # We don't want to fetch all this data a second time in for
        # secondary sections
        if self.processed_primary:
            registrations = []
            for registration in section.registrations:

                if is_registration_to_exclude(registration):
                    continue
                registrations.append(registration.person.uwregid)

            section_data["registrations"] = registrations
            return

        self.processed_primary = True
        access_token = id_photo_token.get_token()
        registration_list = self._get_reg_for_section(
            section.registrations, access_token)
        section_data["registrations"] = registration_list

        try:
            for joint_section in section_data["joint_sections"]:
                joint_section["registrations"] = \
                    self._get_reg_for_section(
                        joint_section["registrations"], access_token)
        except KeyError:
            pass

    def _get_reg_for_section(self, registration_list, access_token):
        registrations = []
        for registration in registration_list:
            if is_registration_to_exclude(registration):
                continue

            # MUWM-5466
            regid = registration.regid
            majors = []
            for major in registration.majors:
                majors.append(major.json_data())
            reg = {
                "class_code": registration.class_code,
                "class_level": registration.class_level,
                "credits": registration.credits,
                "is_auditor": registration.is_auditor,
                "is_independent_start": registration.is_independent_start,
                "majors": majors,
                "photo_url": photo_url(regid, access_token),
                "regid": regid
            }
            for field in ["start_date", "end_date"]:
                if registration.is_independent_start:
                    date = getattr(registration, field)
                    reg[field] = date.strftime("%m/%d/%Y")
                else:
                    reg[field] = ""

            swsperson = registration.person  # SwsPerson object
            if swsperson:
                reg.update(
                    {
                        "email": swsperson.email,
                        "first_name": swsperson.first_name,
                        "surname": swsperson.last_name,
                        "netid": swsperson.uwnetid,
                        "pronouns": swsperson.pronouns,
                        "student_number": swsperson.student_number,
                    }
                )

            registrations.append(reg)
        return registrations


@method_decorator(login_required, name='dispatch')
class InstSectionDetails(OpenInstSectionDetails):
    """
    api: api/v1/instructor_section_details/section_id
    """
    def is_authorized_for_section(self, request, schedule):
        if len(schedule.sections):
            check_section_instructor(schedule.sections[0], schedule.person)
