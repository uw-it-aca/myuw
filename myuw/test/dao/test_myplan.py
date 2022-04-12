# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.dao.myplan import get_plan
from myuw.test import get_request_with_user


class TestMyPlanDao(TestCase):

    def test_get_plan(self):
        req = get_request_with_user('eight')
        data = get_plan(req, 2013, 'summer')
        self.assertEquals(data['terms'][0]['year'], 2013)
        self.assertEquals(data['terms'][0]['quarter'], 'Summer')
        self.assertEquals(len(data["terms"][0]["courses"]), 3)
        self.assertEquals(data["terms"][0]["unready_count"], 3)

        req = get_request_with_user('jinter')
        data = get_plan(req, 2013, 'autumn')
        self.assertEquals(data['terms'][0]['year'], 2013)
        self.assertEquals(data['terms'][0]['quarter'], 'Autumn')
        self.assertEquals(len(data["terms"][0]["courses"]), 5)
        self.assertTrue(data["terms"][0]["has_unready_courses"])
        self.assertFalse(data["terms"][0]["has_ready_courses"])
        self.assertFalse(data["terms"][0]["has_sections"])
        self.assertEquals(data["terms"][0]["ready_count"], 0)
        self.assertEquals(data["terms"][0]["unready_count"], 5)

        data = get_plan(req, 2013, 'spring')
        self.assertEquals(len(data["terms"][0]["courses"]), 6)
        self.assertFalse(data["terms"][0]["has_unready_courses"])
        self.assertTrue(data["terms"][0]["has_ready_courses"])
        self.assertTrue(data["terms"][0]["has_sections"])
        self.assertEquals(data["terms"][0]["ready_count"], 6)
        self.assertEquals(data["terms"][0]["unready_count"], 0)

    def test_error(self):
        req = get_request_with_user('jerror')
        self.assertRaises(
            Exception, get_plan, req, 2013, 'spring')
