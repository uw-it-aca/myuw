# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.dao.campus_building import (
    get_building_by_code, get_buildings_by_schedule)
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.term import get_current_quarter
from myuw.models import CampusBuilding
from myuw.test import get_request_with_date, get_request_with_user


class TestBuildings(TestCase):

    def test_get_by_code(self):
        building = get_building_by_code('PAA')
        self.assertEqual(building.longitude, -122.304747)
        self.assertEqual(
            building.json_data(),
            {
                'code': 'PAA',
                'latitude': 47.6536929997,
                'longitude': -122.304747,
                'name': 'Mechanical Engineering Building',
                'number': '1347'
            })

        self.assertTrue(CampusBuilding.exists('PAA'))
        self.assertIsNotNone(get_building_by_code('PAA'))
        self.assertIsNone(get_building_by_code(''))
        self.assertIsNone(get_building_by_code('*'))
        self.assertIsNone(get_building_by_code(None))

    def test_get_by_schedule(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-08-01"))
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)

        buildings = get_buildings_by_schedule(schedule)
        self.assertEqual(len(buildings), 2)
