# Copyright 2021 UW-IT, University of Washington
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
            "uwregid": "ABC", "year": "2013", "quarter": "spring"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/restclients/view/myplan/student/api/plan/v1/2013,spring,1,ABC")

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
        response = self.client.post(url, {"student_id": "123456"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/iasystem_uw/api/" +
            "v1/evaluation?student_id=123456"))

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
            "id": "12345", "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/grad/services/" +
            "students/v1/api/committee?id=12345"))

        # notices
        url = reverse("myuw_rest_search", args=["sws", "notices"])
        response = self.client.post(url, {
            "uwregid": "12345678123456781234567812345678",
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/sws/student/v5/notice/" +
            "12345678123456781234567812345678.json"))

        # attest covid19
        url = reverse("myuw_rest_search", args=["attest", "covid19"])
        response = self.client.post(url, {
            "uwregid": "9136CCB8F66711D5BE060004AC494FFE",
            "csrfmiddlewaretoken": "0000000"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (
            "/restclients/view/attest/attestations/v1/covid19/" +
            "9136CCB8F66711D5BE060004AC494FFE"))
