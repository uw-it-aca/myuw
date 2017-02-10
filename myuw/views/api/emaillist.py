import json
import traceback
import logging
from django.http import HttpResponse
from myuw.views.rest_dispatch import RESTDispatch
from restclients.sws.section import get_section_by_label
from myuw.dao.mailman import get_section_email_lists
from myuw.views.rest_dispatch import handle_exception


logger = logging.getLogger(__name__)


class Emaillist(RESTDispatch):

    def GET(self, request, year, quarter,
            curriculum_abbr, course_number, section_id):
        """
        GET returns 200 with email lists for the course
        """
        try:
            email_list_json = get_section_email_lists(
                get_section(year, quarter,
                            curriculum_abbr,
                            course_number,
                            section_id), True)
            return HttpResponse(json.dumps(email_list_json))
        except Exception:
            return handle_exception(logger, timer, traceback)


def get_section(year, quarter, curriculum_abbr, course_number, section_id):
    return get_section_by_label("%s,%s,%s,%s/%s" % (
            year, quarter, curriculum_abbr, course_number, section_id))
