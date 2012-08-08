from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.utils import simplejson as json
from mobility.decorators import mobile_template
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import re
import os
import logging
import time
from sws_dao import Schedule


logger = logging.getLogger('myuw_api.views')

# ------------- RESTDispatch --------------------
# Handles passing on the request to the 
# correct view method based on the request type.
# -----------------------------------------------
class RESTDispatch:
    def run(self, *args, **named_args):
        request = args[0]

        if "GET" == request.META['REQUEST_METHOD']:
            if hasattr(self, "GET"):
                return self.GET(*args, **named_args)
            else:
                return self.invalid_method(*args, **named_args)
        else:
            return self.invalid_method(*args, **named_args)

    def invalid_method(self, *args, **named_args):
        response = HttpResponse("Method not allowed")
        response.status_code = 405
        return response

# ------------- CurQuarterStudentClassScheView --------------------
#
# Performs actions on resource at /api/v1/schedule/current/<regid>.
# GET returns 200 with course section schedule details.
#
# ----------------------------------------
class StudClasScheCurQuarView(RESTDispatch):
    def GET(self, request, regid):
        assert False, regid
        schedule = Schedule(regid).get_curr_quarter_schedule()
        if schedule:
            response = HttpResponse(json.dumps(
                    {'year' : schedule.year,
                     'quarter' : schedule.quarter,
                     }))
            response.status_code = 200
        else:
            response = HttpResponse("Scheulde not found")
            response.status_code = 404
        return response


