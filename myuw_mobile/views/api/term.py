import logging
import json
from django.http import HttpResponse
from myuw_mobile.dao.term import get_current_quarter
from myuw_mobile.views.rest_dispatch import RESTDispatch


class Term(RESTDispatch):
    """
    Performs actions on resource at /api/v1/term/current/.
    """

    def GET(self, request):
        """
        GET returns 200 with the current quarter term data
        """
        return HttpResponse(json.dumps(get_current_quarter(request).json_data()))
