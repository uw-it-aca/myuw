from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
#from django.contrib import auth
#from django.contrib.auth.decorators import login_required
#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect
from django.utils import simplejson as json
from mobility.decorators import mobile_template
#from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import re
import os
import sys
import traceback
import logging

from sws_dao import Schedule
from myuw_api.pws_dao import Person as PersonDAO


class RESTDispatch:
    """
    Handles passing on the request to the
    correct view method based on the request type.
    """
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


class StudClasScheCurQuarView(RESTDispatch):
    """
    Performs actions on resource at /api/v1/schedule/current/.
    """
    def GET(self, request):
        """
        GET returns 200 with course section schedule details.
        """

        person_dao = PersonDAO()
        if not "user_netid" in request.session:
            response = HttpResponse('No user in session')
            response.status_code = 400
            return response
        user_netid = request.session["user_netid"]
        person = person_dao.get_person_by_netid(user_netid)
        regid = person.uwregid

        try:
            schedule_dao = Schedule(regid)
            schedule = schedule_dao.get_curr_quarter_schedule()
            colors = schedule_dao.get_colors_for_schedule(schedule)
        except Exception, message:
            print 'Failed to get current quarter schedule: ', message
            traceback.print_exc(file=sys.stdout)
            response = HttpResponse('Failed to get data from SWS...')
            response.status_code = 500
        else:
            if schedule:
                try:
                    json_data = schedule.json_data()

                    section_index = 0
                    # Since the schedule is restclients, and doesn't know
                    # about color ids, backfill that data
                    for section in schedule.sections:
                        section_data = json_data["sections"][section_index]
                        color = colors[section.section_label()]
                        section_data["color_id"] = color
                        section_index += 1

                    response = HttpResponse(json.dumps(json_data))
                except Exception as ex:
                    print "E: ", ex
                response.status_code = 200
            else:
                response = HttpResponse('No registration found')
                response.status_code = 404
        return response
