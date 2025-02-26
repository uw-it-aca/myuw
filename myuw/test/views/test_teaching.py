# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import skipIf
from django.urls import reverse
from myuw.test.api import missing_url, MyuwApiTest


class TestTeachingMethods(MyuwApiTest):

    @skipIf(missing_url("myuw_teaching_page"), "myuw urls not configured")
    def test_instrucor_access(self):
        url = reverse("myuw_teaching_page")
        self.set_user('bill')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)

    @skipIf(missing_url("myuw_teaching_page",
                        kwargs={}), "myuw urls not configured")
    def test_current_quarter_access(self):
        url = reverse("myuw_teaching_page", kwargs={})
        self.set_user('bill')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['display_term']["year"], 2013)
        self.assertEqual(
            response.context['display_term']["quarter"], 'spring')

    @skipIf(missing_url("myuw_teaching_page",
                        kwargs={'year': '2013', 'quarter': 'summer'}),
            "myuw urls not configured")
    def test_future_quarter_access(self):
        url = reverse("myuw_teaching_page",
                      kwargs={'year': '2013', 'quarter': 'summer'})
        self.set_user('bill')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['display_term']["year"], '2013')
        self.assertEqual(
            response.context['display_term']["quarter"], 'summer')

    def test_url_with_section_index(self):
        url = "/teaching/2013,spring,13#PHYS-122-BS"
        self.set_user('billsea')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['display_term']["year"], '2013')
        self.assertEqual(
            response.context['display_term']["quarter"], 'spring')

    @skipIf(missing_url("myuw_section_page",
                        kwargs={'year': '2013', 'quarter': 'spring',
                                'section': 'TRAIN,101/A'}),
            "myuw urls not configured")
    def test_instructor_section_access(self):
        url = reverse("myuw_section_page",
                      kwargs={'year': '2013', 'quarter': 'spring',
                              'section': 'TRAIN,101/A'})
        self.set_user('bill')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['display_term']["year"], '2013')
        self.assertEqual(response.context['display_term']["quarter"],
                         'spring')
        self.assertEqual(response.context['display_term'],
                         {'quarter': u'spring', 'year': u'2013'})
        self.assertEqual(response.context['section'],
                         "2013,spring,TRAIN,101/A")

        url = reverse("myuw_section_page",
                      kwargs={'year': '2013', 'quarter': 'Spring',
                              'section': 'TRAIN,101/A'})
        self.set_user('bill100')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['section'],
                         "2013,Spring,TRAIN,101/A")
        self.assertEqual(response.context['display_term'],
                         {'quarter': u'Spring', 'year': u'2013'})

    @skipIf(missing_url("myuw_photo_list",
                        kwargs={'year': '2013', 'quarter': 'spring',
                                'section': 'TRAIN,101/A'}),
            "myuw urls not configured")
    def test_instructor_section_photo_access(self):
        url = reverse("myuw_photo_list",
                      kwargs={'year': '2013', 'quarter': 'spring',
                              'section': 'TRAIN,101/A'})
        self.set_user('bill')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['section'],
                         "2013,spring,TRAIN,101/A")
        self.assertEqual(response.context['display_term'],
                         {'quarter': u'spring', 'year': u'2013'})

        url = reverse("myuw_photo_list",
                      kwargs={'year': '2013', 'quarter': 'Spring',
                              'section': 'TRAIN,101/A'})
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['section'],
                         "2013,Spring,TRAIN,101/A")
        self.assertEqual(response.context['display_term'],
                         {'quarter': u'Spring', 'year': u'2013'})

        url = reverse("myuw_photo_list",
                      kwargs={'year': '2017', 'quarter': 'autumn',
                              'section': 'EDC&I,552/A'})
        self.set_user('billsea')
        response = self.client.get(
            url,
            HTTP_USER_AGENT="Lynx/2.8.2rel.1 libwww-FM/2.14")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['section'],
                         "2017,autumn,EDC&I,552/A")
        # /MUWM-3997
        # teaching/2017,autumn,EDC&I,552/A/students
