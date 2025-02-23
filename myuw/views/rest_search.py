# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import re
from rc_django.views.rest_proxy import RestSearchView
from myuw.dao.pws import pws

logger = logging.getLogger(__name__)


class MyUWRestSearchView(RestSearchView):
    def __init__(self):
        super(MyUWRestSearchView, self).__init__()
        self.form_action_url = "myuw_rest_search"

    def get_proxy_url(self, request, service, url):
        """
        Convert form data to actual API urls.
        """
        params = None
        logger.debug(
            "Enter MyUWRestProxyView service: {}, url: {}, GET: {}".format(
                service, url, request.POST))

        if service == "book":
            if "iacourse" == url:
                url = "uw/iacourse_status.json?regid={}".format(
                    get_regid(get_input_value(request.POST, "uwregid")))
            else:
                url = "uw/json_utf8_202007.ubs"
                url = "{}?quarter={}&sln1={}&returnlink=t".format(
                    "uw/json_utf8_202007.ubs",
                    get_input_value(request.POST, "quarter"),
                    get_input_value(request.POST, "sln1"))
        elif service == "canvas":
            regid = get_regid(get_input_value(request.POST, "uwregid"))
            url = (
                f"api/v1/users/sis_user_id:{regid}/enrollments?state[]=active"
                + f"&type[]=StudentEnrollment&page=first&per_page=500"
            )
        elif service == "grad":
            params = self.format_params(request)
            params['id'] = get_student_system_key(params['id'])
        elif service == "hfs":
            url = "myuw/v1/{}".format(
                get_input_value(request.POST, "uwnetid"))
        elif re.match(r'^iasystem', service):
            if url.endswith('/evaluation'):
                index = url.find('/')
                service = 'iasystem_' + url[:index]
                index += 1
                url = url[index:]
                params = self.format_params(request)
                if len(params['instructor_id']) > 0:
                    params['instructor_id'] = get_employee_number(
                        params['instructor_id'].strip())
                if len(params['student_id']) > 0:
                    params['student_id'] = get_student_number(
                        params['student_id'].strip())

        elif service == "myplan":
            url = "plan/v1/{},{},1,{}".format(
                get_input_value(request.POST, "year"),
                get_input_value(request.POST, "quarter"),
                get_regid(get_input_value(request.POST, "uwregid")))

        elif service == "sws" and "course" == url:
            year = get_input_value(request.POST, "year")
            quarter = get_input_value(request.POST, "quarter")
            cabbr = get_input_value(request.POST, "curriculum_abbreviation")
            course_number = get_input_value(request.POST, "course_number")
            sln = get_input_value(request.POST, "sln")
            regid = get_input_value(request.POST, "uwregid")
            if len(regid) > 0:
                regid = get_regid(regid)
                search_by = "Instructor"
            else:
                search_by = ""
            url = (
                f"student/v5/section.json?year={year}&quarter={quarter}&" +
                f"future_terms=2&curriculum_abbreviation={cabbr}&" +
                f"course_number={course_number}&reg_id={regid}&" +
                f"search_by={search_by}&include_secondaries=on&" +
                f"sln={sln}&transcriptable_course=all")
        elif service == "sws" and "student" == url:
            regid = get_regid(get_input_value(request.POST, "uwregid"))
            res = get_input_value(request.POST, "res")
            if "adviser" == res:
                url = f"student/v5/person/{regid}/advisers.json"
            elif "degree" == res:
                url = f"student/v5/person/{regid}/degree.json?deg_status=all"
            elif "enrollment" == res:
                url = "student/v5/{}={}{}".format(
                    "enrollment.json?reg_id",
                    regid,
                    "&transcriptable_course=all&verbose=true")
            elif "financial" == res:
                url = f"student/v5/person/{regid}/financial.json"
            elif "notice" == res:
                url = f"student/v5/notice/{regid}.json"
            elif "person" == res:
                url = f"student/v5/person/{regid}.json"

        elif service == "upass":
            res = get_input_value(request.POST, "res")
            netid = get_input_value(request.POST, "uwnetid")
            if "idcard" == res:
                url = f"idcarddataws/api/person/v1/eligibility/{netid}"
            elif "upass" == res:
                url = f"upassdataws/api/person/v1/membershipstatus/{netid}"

        elif service == "uwnetid":
            if "password" == url:
                url = "nws/v1/uwnetid/{}/password".format(
                    get_input_value(request.POST, "uwnetid"))
            elif "subscription" == url:
                url = "nws/v1/uwnetid/{}/subscription/60,64,105".format(
                    get_input_value(request.POST, "uwnetid"))
        else:
            service, url, params = super().get_proxy_url(request, service, url)

        logger.debug(
            "Exit MyUWRestProxyView url: {}".format(url))
        return service, url, params


def get_input_value(post_req, name):
    if name in post_req and len(post_req[name]):
        return post_req[name].strip()
    return ''


def get_regid(userid):
    if userid and len(userid) == 32:
        return userid
    if userid and len(userid) == 7 and userid.isdigit():
        return pws.get_person_by_student_number(userid).uwregid
    return pws.get_person_by_netid(userid).uwregid


def get_employee_number(userid):
    if userid and userid.isdigit():
        return userid
    return pws.get_person_by_netid(userid).employee_id


def get_student_number(userid):
    if userid and userid.isdigit():
        return userid
    return pws.get_person_by_netid(userid).student_number


def get_student_system_key(userid):
    if userid and userid.isdigit():
        return userid
    return pws.get_person_by_netid(userid).student_system_key
