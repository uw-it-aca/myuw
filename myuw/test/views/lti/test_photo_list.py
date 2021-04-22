# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import skipIf
from django.urls import reverse
from django.test.utils import override_settings
from django.test import RequestFactory
from myuw.views.lti.photo_list import LTIPhotoList
from myuw.test.api import missing_url
from myuw.test.views.lti import MyuwLTITest


class TestLTILaunch(MyuwLTITest):
    @skipIf(missing_url('myuw_lti_photo_list'), 'myuw urls not configured')
    def test_lti_launch(self):
        url = reverse('myuw_lti_photo_list')

        # Invalid http method
        response = self.client.get(
            url, HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEquals(response.status_code, 401)

        # Invalid launch payload
        response = self.client.post(
                url, data={},
                HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEquals(response.status_code, 401)


@override_settings(BLTI_AES_KEY=b"11111111111111111111111111111111",
                   BLTI_AES_IV=b"1111111111111111")
class TestLTIPhotoList(MyuwLTITest):
    def setUp(self):
        self.request = RequestFactory().post(reverse('myuw_lti_photo_list'))
        session = self.client.session
        session.save()
        self.request.session = session

    def test_context_data(self):
        blti_data = {
            'custom_canvas_course_id': 12345,
            'lis_course_offering_sourcedid': '2013-spring-ESS-102-A',
            'custom_canvas_user_id': 123456,
            'context_label': 'ESS 102 A'
        }
        kwargs = {
            'request': self.request,
            'blti_params': blti_data,
        }
        context = LTIPhotoList().get_context_data(**kwargs)
        self.assertEquals(context['lti_course_name'], 'ESS 102 A')
        self.assertEquals(context['section'], '2013-spring-ESS-102-AA')
        self.assertEquals(len(context['sections']), 2)

    def test_context_data_no_sections(self):
        blti_data = {
            'custom_canvas_course_id': 12346,
            'lis_course_offering_sourcedid': '2013-spring-ESS-102-B',
            'custom_canvas_user_id': 123456,
            'context_label': 'ESS 102 B'
        }
        kwargs = {
            'request': self.request,
            'blti_params': blti_data,
        }
        context = LTIPhotoList().get_context_data(**kwargs)
        self.assertEquals(context['lti_course_name'], 'ESS 102 B')
        self.assertEquals(context['section'], '')
        self.assertEquals(len(context['sections']), 0)
