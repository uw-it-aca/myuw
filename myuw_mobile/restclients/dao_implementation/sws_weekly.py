"""
A subclass of the SWS file implementation, allows for specifying the current
week of the term
"""

from restclients.dao_implementation.sws import File, Live
from restclients.mock_http import MockHTTP
from django.conf import settings
from datetime import datetime, timedelta
import json
import re


class ByWeek(File):
    def getURL(self, url, headers):
        response = super(ByWeek, self).getURL(url, headers)
        return _update_term_with_offsets(url, response)


class ByWeekLive(Live):
    def getURL(self, url, headers):
        response = super(ByWeekLive, self).getURL(url, headers)
        return _update_term_with_offsets(url, response)


def _update_term_with_offsets(url, response):
    week_of_term = getattr(settings, "MYUW_WEEK_OF_TERM", 0)

    value = getattr(settings,
                    "MYUW_GRADE_SUBMISSION_DEADLINE_OFFSET_MINUTES", 0)
    submission_offset = value

    last_day_offset = getattr(settings,
                              "MYUW_LAST_DAY_OF_CLASSES_OFFSET_DAYS", 0)
    value = getattr(settings,
                    "MYUW_REGISTRATION_SERVICES_START_OFFSET_DAYS", 0)

    registration_offset = value
    final_exam_end_offset = getattr(settings,
                                    "MYUW_FINAL_EXAM_LAST_DAY_OFFSET_DAYS", 0)
    first_day_offset = getattr(settings, "MYUW_FIRST_DAY_OFFSET", 0)
    period2_start_offset = getattr(settings, "MYUW_PERIOD2_START_OFFSET", 0)

    strptime = datetime.strptime
    now = datetime.now()
    try:
        json_data = json.loads(response.data)
    except Exception as ex:
        return response

    day_format = "%Y-%m-%d"
    datetime_format = "%Y-%m-%dT%H:%M:%S"

    # This is to enable mock data grading.
    if (re.match("/student/v\d/term/current.json", url) or
            re.match("/student/v\d/term/2013,spring.json", url)):
        if submission_offset:
            submission_deadline = now + timedelta(minutes=submission_offset)
            formatted = submission_deadline.strftime(datetime_format)
            json_data["GradeSubmissionDeadline"] = formatted

        if last_day_offset:
            last_day = now + timedelta(days=last_day_offset)
            json_data["LastDayOfClasses"] = last_day.strftime(day_format)

        if registration_offset:
            reg_start = now + timedelta(days=registration_offset)
            formatted = reg_start.strftime(day_format)
            json_data["RegistrationServicesStart"] = formatted

        if final_exam_end_offset:
            final_exam_end = now + timedelta(days=final_exam_end_offset)
            json_data["LastFinalExamDay"] = final_exam_end.strftime(day_format)

        if first_day_offset:
            first_day = now + timedelta(days=first_day_offset)
            json_data["FirstDay"] = first_day.strftime(day_format)

        if period2_start_offset:
            start_day = now + timedelta(days=first_day_offset)
            formatted = first_day.strftime(day_format)
            json_data["RegistrationPeriods"][1]["StartDate"] = formatted

        return_response = MockHTTP()
        return_response.status = response.status
        return_response.data = json.dumps(json_data)
        headers = {}
        for header in response.headers:
            headers[header] = response.getheader(header)

        return_response.headers = headers
        return return_response

    if (re.match("/student/v\d/term/next.json", url) or
            re.match("/student/v\d/term/2013,summer.json", url)):
        if period2_start_offset:
            start_day = now + timedelta(days=period2_start_offset)
            formatted = start_day.strftime(day_format)
            json_data["RegistrationPeriods"][1]["StartDate"] = formatted

        return_response = MockHTTP()
        return_response.status = response.status
        return_response.data = json.dumps(json_data)
        headers = {}
        for header in response.headers:
            headers[header] = response.getheader(header)

        return_response.headers = headers
        return return_response

    return response
