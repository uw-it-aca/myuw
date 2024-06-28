# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# -*- coding: utf-8 -*-
from django.test.utils import override_settings
from django.urls import reverse
from myuw.test.api import MyuwApiTest


@override_settings(
    RESTCLIENTS_ADMIN_AUTH_MODULE='rc_django.tests.can_proxy_restclient')
class RestSearchViewTest(MyuwApiTest):

    def test_post(self):
        self.set_user('javerage')

        # hfs
        url = reverse("myuw_rest_search", args=["hfs", "accounts"])
        response = self.client.post(url, {"uwnetid": "javerage"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/restclients/view/hfs/myuw/v1/javerage")

        # bookstore
        url = reverse("myuw_rest_search", args=["book", "index"])
        response = self.client.post(url, {
            "sln1": "123", "quarter": "spring", "returnlink": "t"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/book/uw/json_utf8_202007.ubs%3F"
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

        # upass
        url = reverse("myuw_rest_search", args=["upass", "index"])
        response = self.client.post(url, {
            "uwnetid": "bill",
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/restclients/view/upass/upassdataws/" +
            "api/person/v1/membershipstatus/bill")
