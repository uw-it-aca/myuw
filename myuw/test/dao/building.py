from django.test import TestCase
import datetime
from myuw.dao.building import get_building_by_code, \
    get_buildings_by_schedule
from myuw.dao.schedule import _get_schedule
from restclients.models.sws import Term


class TestBuildings(TestCase):

    def test_get_by_code(self):
        building = get_building_by_code('ELC')
        self.assertEquals(building.longitude, -122.156049)

    def test_get_by_schedule(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2012
        term.quarter = "summer"
        schedule = _get_schedule(regid, term)

        buildings = get_buildings_by_schedule(schedule)
        self.assertEquals(len(buildings), 3)

        term.year = 2001
        schedule = _get_schedule(regid, term)

        buildings = get_buildings_by_schedule(schedule)
        self.assertEquals(buildings, None)
