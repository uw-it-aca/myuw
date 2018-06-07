import re
import logging
import traceback
from datetime import date, datetime
from blti import BLTI
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from myuw.dao import coda
from myuw.views.error import \
    handle_exception, not_instructor_error, data_not_found
from restclients_core.exceptions import DataFailureException
from uw_sws.enrollment import get_enrollment_by_regid_and_term
from uw_sws.person import get_person_by_regid
from myuw.dao.canvas import sws_section_label
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.dao.enrollment import get_code_for_class_level
from myuw.dao.instructor_schedule import \
    check_section_instructor, get_instructor_section
from myuw.dao.pws import get_person_of_current_user, get_url_key_for_regid,\
    get_person_by_regid as get_pws_person_by_regid
from myuw.logger.logresp import log_success_response
from myuw.logger.timer import Timer
from myuw.util.thread import Thread, ThreadWithResponse
from myuw.views.api import OpenAPI
from myuw.views.decorators import blti_admin_required
from myuw.views.api.instructor_schedule import load_schedule, \
    _set_current_or_future

logger = logging.getLogger(__name__)


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
        section_id = kwargs.get('section_id')
        timer = Timer()
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
        self.person = get_person_of_current_user(request)  # pws

        try:
            section_id = self.validate_section_id(request, section_id)
        except NotSectionInstructorException:
            return not_instructor_error()

        schedule = get_instructor_section(request, section_id,
                                          include_registrations=True,
                                          include_linked_sections=True)

        try:
            self.is_authorized_for_section(request, schedule)
        except NotSectionInstructorException:
            return not_instructor_error()

        self.term = schedule.term
        resp_data = load_schedule(request, schedule,
                                  section_callback=self.per_section_data)

        _set_current_or_future(self.term, request, resp_data)

        # Concurrently fetch section data and ICD data
        threads = []

        t = Thread(target=self.add_linked_section_data,
                   args=(resp_data,))
        threads.append(t)
        t.start()

        for section in resp_data['sections']:
            _set_current_or_future(schedule.term, request, section)

            t = Thread(target=coda.get_classlist_details,
                       args=(section['section_label'],
                             section,))

            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        self.add_linked_section_data(resp_data)
        log_success_response(logger, timer)

        return self.json_response(resp_data)

    def validate_section_id(self, request, section_id):
        return section_id

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
                registrations.append(registration.person.uwregid)

            section_data["registrations"] = registrations
            return

        self.processed_primary = True
        registrations = {}
        name_threads = {}
        enrollment_threads = {}

        for registration in section.registrations:
            person = registration.person  # pws person
            regid = person.uwregid

            name_email_thread = ThreadWithResponse(target=self.get_person_info,
                                                   args=(regid,))
            enrollment_thread = ThreadWithResponse(target=self.get_enrollments,
                                                   args=(regid,))

            name_threads[regid] = name_email_thread
            enrollment_threads[regid] = enrollment_thread
            name_email_thread.start()
            enrollment_thread.start()

            email1 = None
            if len(person.email_addresses):
                email1 = person.email_addresses[0]

            reg = {
                    'full_name': person.display_name,
                    'netid': person.uwnetid,
                    'regid': person.uwregid,
                    'student_number': person.student_number,
                    'credits': registration.credits,
                    'is_auditor': registration.is_auditor,
                    'is_independent_start': registration.is_independent_start,
                    'class_level': person.student_class,
                    'email': email1,
                    'url_key': get_url_key_for_regid(person.uwregid),
                }

            for field in ["start_date", "end_date"]:
                if registration.is_independent_start:
                    date = getattr(registration, field)
                    reg[field] = date.strftime("%m/%d/%Y")
                else:
                    reg[field] = ""

            if regid not in registrations:
                registrations[regid] = [reg]
            else:
                registrations[regid].append(reg)

        registration_list = []
        for regid in name_threads:
            thread = name_threads[regid]
            thread.join()

            for reg in registrations[regid]:
                reg["first_name"] = thread.response["first_name"]
                reg["surname"] = thread.response["surname"]
                reg["email"] = thread.response["email"]

            thread = enrollment_threads[regid]
            thread.join()
            if thread.response:

                for reg in registrations[regid]:
                    reg["majors"] = thread.response["majors"]
                    reg["class_level"] =\
                        thread.response["class_level"]

                code = get_code_for_class_level(thread.response["class_level"])

                for reg in registrations[regid]:
                    reg['class_code'] = code

            registration_list.extend(registrations[regid])
        section_data["registrations"] = registration_list

    def get_person_info(self, regid):
        sws_person = get_person_by_regid(regid)
        try:
            fname = sws_person.first_name.title()
        except AttributeError:
            fname = ""

        return {"first_name": fname,
                "surname": sws_person.last_name.title(),
                "email": sws_person.email}

    def get_enrollments(self, regid):
        enrollment = get_enrollment_by_regid_and_term(regid, self.term)
        majors = []
        for major in enrollment.majors:
            majors.append(major.json_data())

        return {"majors": majors,
                "class_level": enrollment.class_level}


@method_decorator(login_required, name='dispatch')
class InstSectionDetails(OpenInstSectionDetails):
    """
    api: api/v1/instructor_section_details/section_id
    """

    def is_authorized_for_section(self, request, schedule):
        try:
            check_section_instructor(schedule.sections[0], schedule.person)
        except IndexError:
            pass


@method_decorator(blti_admin_required, name='dispatch')
class LTIInstSectionDetails(OpenInstSectionDetails):
    def is_authorized_for_section(self, request, schedule):
        pass

    def validate_section_id(self, request, section_id):
        blti_data = BLTI().get_session(request)
        authorized_sections = blti_data.get('authorized_sections', [])

        if section_id not in authorized_sections:
            raise NotSectionInstructorException

        (sws_section_id, instructor_regid) = sws_section_label(section_id)

        if instructor_regid is not None:
            self.person = get_pws_person_by_regid(instructor_regid)

        return sws_section_id
