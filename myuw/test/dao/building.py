import datetime
from django.test import TestCase
from myuw.dao.building import get_building_by_code, \
    get_buildings_by_schedule
from myuw.dao.registration import get_schedule_by_term
from uw_sws.models import Term
from myuw.test import get_request, get_request_with_user


class TestBuildings(TestCase):

    def setUp(self):
        get_request()

    def test_get_by_code(self):
        building = get_building_by_code('ELC')
        self.assertEquals(building.longitude, -122.156049)

    def test_get_by_schedule(self):
        req = get_request_with_user('javerage')
        term = Term()
        term.year = 2013
        term.quarter = "summer"
        schedule = get_schedule_by_term(req, term)

        buildings = get_buildings_by_schedule(schedule)
        self.assertEquals(len(buildings), 2)
