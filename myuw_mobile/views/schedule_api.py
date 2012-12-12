from django.http import HttpResponse
import logging
from django.utils import simplejson as json
from myuw_mobile.dao.sws import Quarter, Schedule
from myuw_mobile.dao.canvas import Enrollments
from rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response
from myuw_mobile.logger.logresp import log_success_response
from operator import itemgetter

schedule_dao = Schedule()
quarter_dao = Quarter()

class StudClasScheCurQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/schedule/current/.
    """
    def GET(self, request):
        """
        GET returns 200 with the current quarter course section schedule
        """
        timer = Timer()
        logger = logging.getLogger('myuw_mobile.views.schedule_api.StudClasScheCurQuar.GET')

        schedule = schedule_dao.get_cur_quarter_schedule()
        if schedule is None or not schedule.json_data():
            log_data_not_found_response(logger, timer)
            return HttpResponse({})

        summer_term = ""
        if len(schedule.sections) > 0 and schedule.term.quarter == "summer":
            sumr_tms = schedule_dao.get_registered_summer_terms(schedule.sections)
            if sumr_tms["A_term"] and sumr_tms["B_term"] and sumr_tms["Full_term"] or sumr_tms["A_term"] and sumr_tms["Full_term"] or sumr_tms["B_term"] and sumr_tms["Full_term"] or sumr_tms["A_term"] and sumr_tms["B_term"]:
                summer_term = quarter_dao.get_current_summer_term()
        resp_data = make_sche_api_response(schedule, summer_term)
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))

class StudClasScheFutureQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/schedule/<year>,<quarter>(,<summer_term>)?
    """
    def GET(self, request, year, quarter, summer_term):
        """
        GET returns 200 with course section schedule details of 
        the given year, quarter. 
        Return the course sections of full term and matched term
        if a specific summer-term is given
        """
        timer = Timer()
        logger = logging.getLogger('myuw_mobile.views.schedule_api.StudClasScheFutureQuar.GET')

        term = quarter_dao.get_term(year, quarter.lower())
        if term is not None:
            schedule = schedule_dao.get_schedule(term)

        if schedule is None or not schedule.json_data():
            log_data_not_found_response(logger, timer)
            return HttpResponse({})

        smr_term = ""
        if summer_term and len(summer_term) > 1:
            smr_term = summer_term[1:]
        resp_data = make_sche_api_response(schedule, smr_term[1:])
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(resp_data))


def make_sche_api_response(schedule, summer_term=""):
    #print "quarter=" + schedule.term.quarter
    #print "summer_term=" + summer_term
    if len(schedule.sections) > 0 and schedule.term.quarter == "summer" and summer_term == "A-term" or summer_term == "B-term":
        filtered_sections = []
        for section in schedule.sections:
            if section.summer_term == "Full-term" or section.summer_term == summer_term:
                filtered_sections.append(section)
        schedule.sections = filtered_sections    

    colors = schedule_dao.get_colors_for_schedule(schedule)

    buildings = schedule_dao.get_buildings_for_schedule(schedule)
    
    enrollments = Enrollments().get_enrollments()

    canvas_data_by_course_id = {}
    for enrollment in enrollments:
        canvas_data_by_course_id[enrollment.sws_course_id()] = enrollment

    if colors is None:
        if len(schedule.sections) > 0:
            log_data_not_found_response(logger, timer)
            return data_not_found()
    # Since the schedule is restclients, and doesn't know
    # about color ids, backfill that data
    json_data = schedule.json_data()


    section_index = 0
    for section in schedule.sections:
        section_data = json_data["sections"][section_index]
        color = colors[section.section_label()]
        section_data["color_id"] = color
        section_index += 1

        if section.section_label() in canvas_data_by_course_id:
            enrollment = canvas_data_by_course_id[section.section_label()]
            canvas_url = enrollment.course_url
            canvas_name = enrollment.course_name
            section_data["canvas_url"] = canvas_url
            section_data["canvas_name"] = canvas_name

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
            mdata = section_data["meetings"][meeting_index]
            if not mdata["building_tbd"]:
                building = buildings[mdata["building"]]
                if building is not None:
                    mdata["latitude"] = building.latitude
                    mdata["longitude"] = building.longitude
                    mdata["building_name"] = building.name

            for instructor in mdata["instructors"]:
                if not instructor[
                    "email1"] and not instructor[
                    "email2"] and not instructor[
                    "phone1"] and not instructor[
                    "phone2"] and not instructor[
                    "voicemail"] and not instructor[
                    "fax"] and not instructor[
                    "touchdial"] and not instructor[
                    "address1"] and not instructor[
                    "address2"]:
                    instructor["whitepages_publish"] = False
            meeting_index += 1

    # MUWM-443
    json_data["sections"] = sorted(json_data["sections"],
                                   key=itemgetter('curriculum_abbr',
                                                  'course_number',
                                                  'section_id',
                                                  ))
    json_data["summer_term"]=summer_term
    return json_data
