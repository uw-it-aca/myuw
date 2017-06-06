import datetime
from django.test import TestCase
from myuw.dao.building import get_building_by_code, \
    get_buildings_by_schedule
from myuw.dao.schedule import _get_schedule
from uw_sws.models import Term
from myuw.test import get_request


class TestBuildings(TestCase):

    def setUp(self):
        get_request()

    def test_get_by_code(self):
        building = get_building_by_code('ELC')
        self.assertEquals(building.longitude, -122.156049)

    def test_get_by_schedule(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2013
        term.quarter = "summer"
        schedule = _get_schedule(regid, term)

        buildings = get_buildings_by_schedule(schedule)
        self.assertEquals(len(buildings), 2)
