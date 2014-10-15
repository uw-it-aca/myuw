"""
A subclass of the SWS file implementation, allows for specifying the current
week of the term
"""

from restclients.dao_implementation.sws import File
from django.conf import settings
from datetime import datetime, timedelta
import json
import re

class ByWeek(File):
    def getURL(self, url, headers):
        response = super(ByWeek, self).getURL(url, headers)

        week_of_term = getattr(settings, "MYUW_WEEK_OF_TERM", 0)

        submission_offset = getattr(settings, "MYUW_GRADE_SUBMISSION_DEADLINE_OFFSET_MINUTES", 0)
        last_day_offset = getattr(settings, "MYUW_LAST_DAY_OF_CLASSES_OFFSET_DAYS", 0)
        registration_offset = getattr(settings, "MYUW_REGISTRATION_SERVICES_START_OFFSET_DAYS", 0)
        final_exam_end_offset = getattr(settings, "MYUW_FINAL_EXAM_LAST_DAY_OFFSET_DAYS", 0)
        first_day_offset = getattr(settings, "MYUW_FIRST_DAY_OFFSET", 0)

        # This is to enable mock data grading.
        if re.match("/student/v\d/term/current.json", url) or re.match("/student/v\d/term/2013,spring.json", url):
# This *was* the by week approach.  Now it's just a bunch of dates.  Don't know
# why I'm not just deleting all of this code.  Maybe so you'll remember why
# this was called weekly, when it isn't at all weekly.
#            now = datetime.now()
#
#            if week_of_term > 0:
#                days_delta = (week_of_term - 1) * 7
#            else:
#                days_delta = week_of_term * 7
#
#            start_date = now + timedelta(days=-1*days_delta)
#
#
#            json_data["FirstDay"] = start_date.strftime("%Y-%m-%d")

            strptime = datetime.strptime
            now = datetime.now()
            json_data = json.loads(response.data)
            day_format = "%Y-%m-%d"
            datetime_format = "%Y-%m-%dT%H:%M:%S"

            if submission_offset:
                submission_deadline = now + timedelta(minutes=submission_offset)
                json_data["GradeSubmissionDeadline"] = submission_deadline.strftime(datetime_format)

            if last_day_offset:
                last_day = now + timedelta(days=last_day_offset)
                json_data["LastDayOfClasses"] = last_day.strftime(day_format)

            if registration_offset:
                reg_start = now + timedelta(days=registration_offset)
                json_data["RegistrationServicesStart"] = reg_start.strftime(day_format)

            if final_exam_end_offset:
                final_exam_end = now + timedelta(days=final_exam_end_offset)
                json_data["LastFinalExamDay"] = final_exam_end.strftime(day_format)

            if first_day_offset:
                first_day = now + timedelta(days=first_day_offset)
                json_data["FirstDay"] = first_day.strftime(day_format)

            response.data = json.dumps(json_data)

        return response

