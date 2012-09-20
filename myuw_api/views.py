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

from myuw_mobile.dao.sws import Schedule
from myuw_mobile.dao.pws import Person as PersonDAO
from myuw_mobile.user import UserService
from restclients.bookstore import Bookstore


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


class StudClasScheCurQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/schedule/current/.
    """
    def GET(self, request):
        """
        GET returns 200 with course section schedule details.
        """

        person_dao = PersonDAO()
        user_netid = UserService(request.session).get_user()

        if user_netid is None:
            response = HttpResponse('No user in session')
            response.status_code = 400
            return response

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


class TextbookCurQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/books/current/.
    """
    def GET(self, request):
        """
        GET returns 200 with books for the current quarter
        """

        person_dao = PersonDAO()
        user_netid = UserService(request.session).get_user()

        if user_netid is None:
            response = HttpResponse('No user in session')
            response.status_code = 400
            return response
        person = person_dao.get_person_by_netid(user_netid)
        regid = person.uwregid

        try:
            schedule_dao = Schedule(regid)
            schedule = schedule_dao.get_curr_quarter_schedule()

            books_dao = Bookstore()

            book_data = books_dao.get_books_for_schedule(schedule)
        except Exception, message:
            print 'Failed to get book list: ', message
            traceback.print_exc(file=sys.stdout)
            response = HttpResponse('Failed to get data from SWS...')
            response.status_code = 500
        else:
            if book_data:
                try:
                    json_data = {}

                    for sln in book_data:
                        json_data[sln] = []

                        for book in book_data[sln]:
                            json_data[sln].append(book.json_data())

                    response = HttpResponse(json.dumps(json_data))
                except Exception as ex:
                    print "E: ", ex
                response.status_code = 200
            else:
                response = HttpResponse('No book data found')
                response.status_code = 404
        return response

class InstructorContact(RESTDispatch):
    def GET(self, request, regid):
        """ 
        GET returns 200 with course section schedule details.
        """

        person_dao = PersonDAO()
        person_dao.get_contact(regid)

        person_data = person_dao.get_contact(regid)

        if person_data:
            try:
                if person_data["WhitepagesPublish"] == False:
                    affiliations = person_data["PersonAffiliations"]
                    if "EmployeePersonAffiliation" in affiliations:
                        data = affiliations["EmployeePersonAffiliation"]
                        data["EmployeeWhitePages"] = {}

                    if "StudentPersonAffiliation" in affiliations:
                        data = affiliations["StudentPersonAffiliation"]
                        data["StudentWhitePages"] = {}

                response = HttpResponse(json.dumps(person_data))
            except Exception, message:
                print 'Failed to get instructor data: ', message
                response.status_code = 500 
        return response 
