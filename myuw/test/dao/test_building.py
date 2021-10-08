# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime
from django.test import TestCase
from myuw.dao.building import get_building_by_code, \
    get_buildings_by_schedule
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.term import get_current_quarter
from myuw.test import get_request_with_date, get_request_with_user


class TestBuildings(TestCase):

    def test_get_by_code(self):
        building = get_building_by_code('ELC')
        self.assertEquals(building.longitude, -122.156049)

    def test_get_by_schedule(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-08-01"))
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)

        buildings = get_buildings_by_schedule(schedule)
        self.assertEquals(len(buildings), 2)
