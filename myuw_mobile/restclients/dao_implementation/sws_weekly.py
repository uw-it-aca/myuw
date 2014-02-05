"""
A subclass of the SWS file implementation, allows for specifying the current
week of the term
"""

from restclients.dao_implementation.sws import File
from django.conf import settings
from datetime import datetime, timedelta
import json

class ByWeek(File):
    def getURL(self, url, headers):
        response = super(ByWeek, self).getURL(url, headers)

        week_of_term = getattr(settings, "MYUW_WEEK_OF_TERM", 1)

        # This is to enable mock data grading.
        if "/student/v4/term/current.json" == url or "/student/v4/term/2013,spring.json" == url:
            now = datetime.now()
            if week_of_term > 0:
                days_delta = (week_of_term - 1) * 7
            else:
                days_delta = week_of_term * 7

            start_date = now + timedelta(days=-1*days_delta)

            json_data = json.loads(response.data)

            json_data["FirstDay"] = start_date.strftime("%Y-%m-%d")

            response.data = json.dumps(json_data)

        return response

