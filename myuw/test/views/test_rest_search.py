# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# -*- coding: utf-8 -*-
from django.test.utils import override_settings
from django.urls import reverse
from myuw.test.api import MyuwApiTest
from myuw.views.rest_search import (
    get_input_value, get_regid, get_employee_number, get_student_number,
    get_student_system_key
)


@override_settings(
    RESTCLIENTS_ADMIN_AUTH_MODULE='rc_django.tests.can_proxy_restclient')
class RestSearchViewTest(MyuwApiTest):

    def test_get_regid(self):
        self.assertEqual(
            get_regid("javerage"), "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEqual(
            get_regid("1033334"), "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEqual(
            get_regid("9136CCB8F66711D5BE060004AC494FFE"),
            "9136CCB8F66711D5BE060004AC494FFE")

    def test_get_employee_number(self):
        self.assertEqual(
            get_employee_number("javerage"), "123456789")
        self.assertEqual(
            get_employee_number("123456789"), "123456789")

    def test_get_student_number(self):
        self.assertEqual(
            get_student_number("javerage"), "1033334")
        self.assertEqual(
            get_student_number("1033334"), "1033334")

    def test_get_student_system_key(self):
        self.assertEqual(
            get_student_system_key("javerage"), "000083856")
        self.assertEqual(
            get_student_system_key("000083856"), "000083856")

    def test_post(self):
        self.set_user('javerage')
        self.assertEqual(get_input_value({}, "uwnetid"), "")

        # hfs
        url = reverse("myuw_rest_search", args=["hfs", "accounts"])
        response = self.client.post(url, {"uwnetid": "javerage"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/restclients/view/hfs/myuw/v1/javerage")

        # iacourses
        url = reverse("myuw_rest_search", args=["book", "iacourse"])
        response = self.client.post(url, {"uwregid": "javerage"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/book/uw/iacourse_status.json%3Fregid="
            "9136CCB8F66711D5BE060004AC494FFE"))

        # book
        url = reverse("myuw_rest_search", args=["book", "index"])
        response = self.client.post(url, {
            "sln1": "123", "quarter": "spring", "returnlink": "t"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/book/uw/json_utf8_202507.ubs%3F"
            "quarter=spring&sln1=123&returnlink=t"))

        # myplan
        url = reverse("myuw_rest_search", args=["myplan", "index"])
        response = self.client.post(url, {
            "uwregid": "javerage", "year": "2013", "quarter": "spring"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/restclients/view/myplan/plan/v1/2013,spring,1," +
            "9136CCB8F66711D5BE060004AC494FFE")

        # libraries
        url = reverse("myuw_rest_search", args=["libraries", "accounts"])
        response = self.client.post(url, {"id": "javerage"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/restclients/view/libraries/mylibinfo/v1/?id=javerage")

        # iasystem
        url = reverse("myuw_rest_search", args=[
            "iasystem_uw", "uw/api/v1/evaluation"])
        response = self.client.post(
            url,
            {
                'term_name': 'Winter', 'curriculum_abbreviation': 'TRAIN',
                'course_number': '100', 'section_id': 'A', 'year': '2013',
                'instructor_id': '', 'student_id': 'javerage'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/iasystem_uw/api/v1/evaluation?term_name=" +
            "Winter&curriculum_abbreviation=TRAIN&course_number=100&" +
            "section_id=A&year=2013&instructor_id=&student_id=1033334"))

        response = self.client.post(
            url,
            {
                'term_name': 'Winter', 'curriculum_abbreviation': 'TRAIN',
                'course_number': '100', 'section_id': 'A', 'year': '2013',
                'instructor_id': 'bill', 'student_id': ''
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/iasystem_uw/api/v1/evaluation?term_name=" +
            "Winter&curriculum_abbreviation=TRAIN&course_number=100&" +
            "section_id=A&year=2013&instructor_id=123456782&student_id="))

        # uwnetid
        url = reverse("myuw_rest_search", args=["uwnetid", "password"])
        response = self.client.post(url, {"uwnetid": "javerage"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/restclients/view/uwnetid/nws/v1/uwnetid/javerage/password")

        url = reverse("myuw_rest_search", args=["uwnetid", "subscription"])
        response = self.client.post(url, {"uwnetid": "javerage"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/restclients/view/uwnetid/nws/v1/uwnetid/" +
            "javerage/subscription/60,64,105")

        # grad
        url = reverse("myuw_rest_search", args=[
            "grad", "services/students/v1/api/committee"])
        response = self.client.post(url, {
            "id": "seagrad", "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/grad/services/" +
            "students/v1/api/committee?id=001000002"))

        # notices
        url = reverse("myuw_rest_search", args=["sws", "student"])
        response = self.client.post(url, {
            "uwregid": "12345678123456781234567812345678",
            "res": 'notice',
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/sws/student/v5/notice/" +
            "12345678123456781234567812345678.json"))

        # person
        url = reverse("myuw_rest_search", args=["sws", "student"])
        response = self.client.post(url, {
            "uwregid": "12345678123456781234567812345678",
            "res": 'person',
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/sws/student/v5/person/" +
            "12345678123456781234567812345678.json"))

        # degree
        url = reverse("myuw_rest_search", args=["sws", "student"])
        response = self.client.post(url, {
            "uwregid": "12345678123456781234567812345678",
            "res": 'degree',
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/sws/student/v5/person/" +
            "12345678123456781234567812345678/degree.json%3Fdeg_status=all"))

        # adviser
        url = reverse("myuw_rest_search", args=["sws", "student"])
        response = self.client.post(url, {
            "uwregid": "12345678123456781234567812345678",
            "res": 'adviser',
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/sws/student/v5/person/" +
            "12345678123456781234567812345678/advisers.json"))

        # Financial
        url = reverse("myuw_rest_search", args=["sws", "student"])
        response = self.client.post(url, {
            "uwregid": "12345678123456781234567812345678",
            "res": 'financial',
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/sws/student/v5/person/" +
            "12345678123456781234567812345678/financial.json"))
        self.maxDiff = None

        # enrollment
        url = reverse("myuw_rest_search", args=["sws", "student"])
        response = self.client.post(url, {
            "uwregid": "javerage",
            "res": 'enrollment',
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/sws/student/v5/enrollment.json%3Freg_id=" +
            "9136CCB8F66711D5BE060004AC494FFE&" +
            "transcriptable_course=all&verbose=true"))

        # Course section
        url = reverse("myuw_rest_search", args=["sws", "course"])
        response = self.client.post(url, {
            "uwregid": "12345678123456781234567812345678",
            "quarter": 'spring',
            "year": 2013,
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/sws/student/v5/section.json%3Fyear=2013&" +
            "quarter=spring&future_terms=2&curriculum_abbreviation=&" +
            "course_number=&reg_id=12345678123456781234567812345678&" +
            "search_by=Instructor&include_secondaries=on&" +
            "sln=&transcriptable_course=all"))
        response = self.client.post(url, {
            "sln": "12345",
            "quarter": 'spring',
            "year": 2013,
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/sws/student/v5/section.json%3Fyear=2013&" +
            "quarter=spring&future_terms=2&curriculum_abbreviation=&" +
            "course_number=&reg_id=&search_by=&include_secondaries=on&" +
            "sln=12345&transcriptable_course=all"))

        # upass
        url = reverse("myuw_rest_search", args=["upass", "index"])
        response = self.client.post(url, {
            "uwnetid": "bill",
            "res": "upass",
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/restclients/view/upass/upassdataws/" +
            "api/person/v1/membershipstatus/bill")

        # idcard
        url = reverse("myuw_rest_search", args=["upass", "index"])
        response = self.client.post(
            url, {"uwnetid": "bill",
                  "res": "idcard",
                  "csrfmiddlewaretoken": "0000000"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/restclients/view/upass/idcarddataws/"
            + "api/person/v1/eligibility/bill",
        )
