from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import re
import traceback
from myuw.views.error import (
    handle_exception, not_instructor_error, data_not_found)
import logging
from operator import itemgetter
from restclients_core.exceptions import DataFailureException
from uw_iasystem.exceptions import TermEvalNotCreated
from uw_sws.person import get_person_by_regid
from uw_sws.enrollment import get_enrollment_by_regid_and_term
from uw_sws.term import get_specific_term
from uw_gradepage.grading_status import get_grading_status
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.dao.building import get_buildings_by_schedule
from myuw.dao.canvas import get_canvas_course_url, sws_section_label
from myuw.dao.course_color import get_colors_by_schedule
from myuw.dao.enrollment import get_code_for_class_level
from myuw.dao.gws import is_grad_student
from myuw.dao.iasystem import get_evaluation_by_section_and_instructor
from myuw.dao.instructor_schedule import (
    get_instructor_schedule_by_term, get_limit_estimate_enrollment_for_section,
    get_instructor_section, get_primary_section, check_section_instructor)
from myuw.dao.library import get_subject_guide_by_section
from myuw.dao.mailman import get_section_email_lists
from myuw.dao.pws import (
    get_person_of_current_user, get_person_by_regid as get_pws_person_by_regid,
    get_url_key_for_regid)
from myuw.dao.registration import get_active_registrations_for_section
from myuw.dao.term import (
    get_current_quarter, is_past, is_future, get_previous_number_quarters,
    get_future_number_quarters)
from myuw.logger.logresp import log_success_response
from myuw.logger.logback import log_exception
from myuw.logger.timer import Timer
from myuw.util.thread import Thread, ThreadWithResponse
from myuw.views.api import OpenAPI, ProtectedAPI
from myuw.views.api.base_schedule import irregular_start_end
from myuw.views.decorators import blti_admin_required
from blti import BLTI

logger = logging.getLogger(__name__)
EARLY_FALL_START = "EARLY FALL START"
MYUW_PRIOR_INSTRUCTED_TERM_YEARS_DEFAULT = 6
MYUW_FUTURE_INSTRUCTED_TERM_COUNT_DEFAULT = 2


class InstSche(ProtectedAPI):
    def make_http_resp(self, timer, term, request, summer_term=None):
        """
        @return instructor schedule data in json format
                status 404: no schedule found (teaching no courses)
        """
        schedule = get_instructor_schedule_by_term(term)
        resp_data = load_schedule(request, schedule)
        log_success_response(logger, timer)
        return self.json_response(resp_data)


def set_classroom_info_url(meeting):
    if len(meeting.building) and meeting.building != "*" and\
            len(meeting.room_number) and meeting.room_number != "*":
        return 'http://www.washington.edu/classroom/%s+%s' % (
            meeting.building, meeting.room_number)
    return None


def set_secondary_final_exam(secondary_section):
    try:
        primary_section = get_primary_section(secondary_section)
        if primary_section and primary_section.final_exam:
            return primary_section.final_exam.json_data()
    except Exception:
        log_exception(
            logger, 'set_secondary_final_exam', traceback.format_exc())
    return secondary_section.final_exam.json_data()


def set_section_grading_status(section, person):
    try:
        section_id = '-'.join([
            section.term.canvas_sis_id(),
            section.curriculum_abbr.upper(),
            section.course_number,
            section.section_id.upper(),
            person.uwregid
        ])
        return get_grading_status(
            section_id, act_as=person.uwnetid).json_data()
    except DataFailureException as ex:
        if ex.status == 400 or ex.status == 404:
            return None
        else:
            raise
    except Exception:
        log_exception(
            logger, 'get_section_grading_status', traceback.format_exc())


def set_section_evaluation(section, person):
    try:
        evaluations = get_evaluation_by_section_and_instructor(
            section, person.employee_id)
        if evaluations is not None:
            for eval in evaluations:
                if section.sln and eval.section_sln == section.sln:
                    return eval.json_data()
        return {'eval_not_exist': True}
    except DataFailureException as ex:
        if isinstance(ex, TermEvalNotCreated):
            # eval not created for the term
            return {'eval_not_exist': True}

        if ex.status != 404:
            log_exception(
                logger, 'set_section_evaluation', traceback.format_exc())


def set_course_resources(section_data, section, person):
    threads = []
    t = ThreadWithResponse(target=get_canvas_course_url,
                           args=(section, person))
    t.start()
    threads.append((t, 'canvas_url', section_data))

    if section.sln:
        t = ThreadWithResponse(target=get_subject_guide_by_section,
                               args=(section,))
        t.start()
        threads.append((t, 'lib_subj_guide', section_data))

    t = ThreadWithResponse(target=get_section_email_lists,
                           args=(section, True))
    t.start()
    threads.append((t, 'email_list', section_data))

    t = ThreadWithResponse(target=set_section_grading_status,
                           args=(section, person,))
    t.start()
    threads.append((t, 'grading_status', section_data))

    t = ThreadWithResponse(target=set_section_evaluation,
                           args=(section, person,))
    t.start()
    threads.append((t, 'evaluation', section_data))

    for i, meeting in enumerate(section.meetings):
        t = ThreadWithResponse(target=set_classroom_info_url,
                               args=(meeting,))
        t.start()
        threads.append((t, 'classroom_info_url', section_data['meetings'][i]))

    if section.final_exam and section.final_exam.building:
        t = ThreadWithResponse(target=set_classroom_info_url,
                               args=(section.final_exam,))
        t.start()
        threads.append((t, 'classroom_info_url', section_data['final_exam']))

    if not section.is_primary_section:
        t = ThreadWithResponse(target=set_secondary_final_exam,
                               args=(section,))
        t.start()
        threads.append((t, 'final_exam', section_data))

    if not hasattr(section, 'limit_estimate_enrollment'):
        t = ThreadWithResponse(
            target=get_limit_estimate_enrollment_for_section,
            args=(section,))
        t.start()
        threads.append((t, 'limit_estimate_enrollment', section_data))

    for t, k, d in threads:
        t.join()
        if t.exception is None:
            d[k] = t.response
        else:
            logger.error("%s: %s" % (k, t.exception))


def set_indep_study_section_enrollments(section, section_json_data):
    """
    for the instructor (current user)
    """
    if (not section.sln or not section.current_enrollment or
            not section.is_independent_study):
        return
    try:
        registrations = get_active_registrations_for_section(
            section, section_json_data['independent_study_instructor_regid'])
        total_enrollment = len(registrations)
        if total_enrollment < section.current_enrollment:
            section_json_data['current_enrollment'] = total_enrollment
        if total_enrollment == 1:
            person = registrations[0].person
            section_json_data['enrollment_student_name'] =\
                "%s, %s" % (person.surname.title(), person.first_name.title())
    except DataFailureException as ex:
        if ex.status == 404:
            section_json_data['current_enrollment'] = 0
        else:
            raise
    except Exception:
        log_exception(logger,
                      'set_indep_study_section_enrollments',
                      traceback.format_exc())


def safe_label(label):
    return re.sub(r"[^A-Za-z0-9]", "_", label)


def load_schedule(request, schedule, summer_term="", section_callback=None):

    json_data = schedule.json_data()

    json_data["summer_term"] = summer_term

    json_data["related_terms"] = _load_related_terms(request)
    json_data["past_term"] = is_past(schedule.term, request)
    json_data["future_term"] = is_future(schedule.term, request)

    json_data["grading_period_is_open"] =\
        schedule.term.is_grading_period_open()
    json_data["grading_period_is_past"] =\
        schedule.term.is_grading_period_past()

    colors = get_colors_by_schedule(schedule)

    buildings = get_buildings_by_schedule(schedule)

    # Since the schedule is restclients, and doesn't know
    # about color ids, backfill that data
    section_index = 0
    course_resource_threads = []
    for section in schedule.sections:
        section_data = json_data["sections"][section_index]

        section_data["section_type"] = section.section_type
        if section.section_label() in colors:
            color = colors[section.section_label()]
            section_data["color_id"] = color
        section_index += 1

        section_data["section_label"] =\
            safe_label(section.section_label())

        if section.is_primary_section:
            if section.linked_section_urls:
                section_data["total_linked_secondaries"] =\
                    len(section.linked_section_urls)
        else:
            section_data["primary_section_label"] =\
                safe_label(section.primary_section_label())

        if section.is_independent_study:
            section_data['is_independent_study'] = True
            section_data['independent_study_instructor_regid'] =\
                schedule.person.uwregid

            set_indep_study_section_enrollments(section, section_data)
        else:
            section_data['is_independent_study'] = False

        section_data[
            'allows_secondary_grading'] = section.allows_secondary_grading

        if section.is_early_fall_start():
            section_data["cc_display_dates"] = True
            section_data["early_fall_start"] = True
            json_data["has_early_fall_start"] = True
        else:
            if section.is_campus_pce():
                group_independent_start = irregular_start_end(
                    schedule.term, section, section.summer_term)
                if group_independent_start:
                    section_data["cc_display_dates"] = True

        # if section.is_primary_section:
        section_data['grade_submission_delegates'] = []
        for delegate in section.grade_submission_delegates:
            section_data['grade_submission_delegates'].append(
                {
                    'person': delegate.person.json_data(),
                    'level': delegate.delegate_level
                })

        t = Thread(target=set_course_resources, args=(
            section_data, section, schedule.person))
        course_resource_threads.append(t)
        t.start()

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

        if section_callback:
            section_callback(section, section_data)

    for t in course_resource_threads:
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


def _load_related_terms(request):
    current_term = get_current_quarter(request)
    terms = []

    prior_years = getattr(settings, "MYUW_PRIOR_INSTRUCTED_TERM_YEARS",
                          MYUW_PRIOR_INSTRUCTED_TERM_YEARS_DEFAULT)
    for term in get_previous_number_quarters(request, prior_years * 4):
        terms.append(term.json_data())

    terms.append(current_term.json_data())

    future_terms = getattr(settings, "MYUW_FUTURE_INSTRUCTED_TERM_COUNT",
                           MYUW_FUTURE_INSTRUCTED_TERM_COUNT_DEFAULT)
    for term in get_future_number_quarters(request, future_terms):
        terms.append(term.json_data())

    return terms


class InstScheCurQuar(InstSche):
    """
    Performs actions on resource at /api/v1/instructor_schedule/current/
    """
    def get(self, request, *args, **kwargs):
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
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with a specific term instructor schedule
        @return course schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        year = kwargs.get("year")
        quarter = kwargs.get("quarter")
        summer_term = kwargs.get("summer_term", None)
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


class InstSect(ProtectedAPI):
    """
    Performs actions on resource at
    /api/v1/instructor_section/<year>,<quarter>,<curriculum>,
        <course_number>,<course_section>?
    """
    def is_authorized_for_section(self, request, schedule):
        try:
            check_section_instructor(schedule.sections[0], schedule.person)
        except IndexError:
            pass

    def make_http_resp(self, timer, request, section_id):
        """
        @return instructor schedule data in json format
                status 404: no schedule found (teaching no courses)
        """
        person = get_person_of_current_user()
        schedule = get_instructor_section(person, section_id)

        try:
            self.is_authorized_for_section(request, schedule)
        except NotSectionInstructorException:
            return not_instructor_error()

        resp_data = load_schedule(request, schedule)
        log_success_response(logger, timer)
        return self.json_response(resp_data)

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with a specific term instructor schedule
        @return course schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        section_id = kwargs.get("section_id")
        timer = Timer()
        try:
            return self.make_http_resp(timer, request, section_id)
        except Exception:
            return handle_exception(logger, timer, traceback)


class OpenInstSectionDetails(OpenAPI):
    """
    Performs actions on resource at
    /api/v1/instructor_section/<year>,<quarter>,<curriculum>,
        <course_number>,<course_section>?
    """
    def validate_section_id(self, request, section_id):
        return section_id

    def is_authorized_for_section(self, request, schedule):
        raise NotSectionInstructorException()

    def make_http_resp(self, timer, request, section_id):
        """
        @return instructor schedule data in json format
            status 404: no schedule found (teaching no courses)
        """
        self.processed_primary = False
        self.person = get_person_of_current_user()

        try:
            section_id = self.validate_section_id(request, section_id)
        except NotSectionInstructorException:
            return not_instructor_error()

        schedule = get_instructor_section(self.person, section_id,
                                          include_registrations=True,
                                          include_linked_sections=True)

        try:
            self.is_authorized_for_section(request, schedule)
        except NotSectionInstructorException:
            return not_instructor_error()

        self.term = schedule.term
        resp_data = load_schedule(request, schedule,
                                  section_callback=self.per_section_data)

        self.add_linked_section_data(resp_data)
        log_success_response(logger, timer)

        return self.json_response(resp_data)

    def add_linked_section_data(self, resp_data):
        section_types = {}
        sections_for_user = {}
        all_types = set()
        for section in resp_data["sections"][1:]:
            section_id = section["section_id"]
            section_type = section["section_type"]
            section_types[section_id] = section_type
            all_types.add(section_type)
            for registration in section["registrations"]:
                if registration not in sections_for_user:
                    sections_for_user[registration] = []
                sections_for_user[registration].append(section_id)

        for registration in resp_data["sections"][0]["registrations"]:
            regid = registration["regid"]
            registration["linked_sections"] = []
            if regid in sections_for_user:
                user_types = {}
                for section in sections_for_user[regid]:
                    section_type = section_types[section]

                    if section_type not in user_types:
                        user_types[section_type] = []

                    user_types[section_type].append(section)

                for section_type in sorted(all_types):
                    # These are for sorting
                    if section_type in user_types:
                        sort_string = ",".join(user_types[section_type])
                        registration["linked_sections"].append(
                            {'type': section_type,
                             'sections': user_types[section_type]})
                    else:
                        sort_string = "ZZ"
                        registration["linked_sections"].append(
                            {'type': section_type,
                             'sections': [""]})
                    registration["linked_type_"+section_type] = sort_string

        types_list = list(set(section_types.values()))
        resp_data["sections"][0]["linked_types"] = types_list

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
            person = registration.person
            regid = person.uwregid

            name_email_thread = ThreadWithResponse(target=self.get_person_info,
                                                   args=(person,))
            enrollment_thread = ThreadWithResponse(target=self.get_enrollments,
                                                   args=(person,))

            name_threads[regid] = name_email_thread
            enrollment_threads[regid] = enrollment_thread
            name_email_thread.start()
            enrollment_thread.start()

            registrations[regid] = {
                'full_name': person.display_name,
                'netid': person.uwnetid,
                'regid': person.uwregid,
                'student_number': person.student_number,
                'credits': registration.credits,
                'class': person.student_class,
                'email': person.email1,
                'url_key': get_url_key_for_regid(person.uwregid),
            }

        registration_list = []
        for regid in name_threads:
            thread = name_threads[regid]
            thread.join()
            registrations[regid]["name"] = thread.response["name"]
            registrations[regid]["surname"] = thread.response["surname"]
            registrations[regid]["email"] = thread.response["email"]

            thread = enrollment_threads[regid]
            thread.join()
            if thread.response:
                registrations[regid]["majors"] = thread.response["majors"]
                registrations[regid]["class"] = thread.response["class"]

                code = get_code_for_class_level(thread.response["class"])
                registrations[regid]['class_code'] = code

            registration_list.append(registrations[regid])
        section_data["registrations"] = registration_list

    def get_person_info(self, person):
        sws_person = get_person_by_regid(person.uwregid)
        return {"name": sws_person.first_name.title(),
                "surname": sws_person.last_name.title(),
                "email": sws_person.email
                }

    def get_enrollments(self, person):
        regid = person.uwregid

        enrollments = get_enrollment_by_regid_and_term(regid, self.term)
        majors = []
        for major in enrollments.majors:
            majors.append(major.json_data())

        return {"majors": majors, "class": enrollments.class_level}

    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with a specific term instructor schedule
        @return course schedule data in json format
                status 404: no schedule found (not registered)
                status 543: data error
        """
        section_id = kwargs.get('section_id')
        timer = Timer()
        try:
            return self.make_http_resp(timer, request, section_id)
        except Exception as ex:
            return handle_exception(logger, timer, traceback)


@method_decorator(login_required, name='dispatch')
class InstSectionDetails(OpenInstSectionDetails):
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
