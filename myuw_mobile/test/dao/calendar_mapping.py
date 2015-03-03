from django.test import TestCase
from django.test.client import RequestFactory
from myuw_mobile.dao.calendar_mapping import \
    get_calendars_for_minors, get_calendars_for_majors, \
    get_calendars_for_gradmajors, _get_enrollments


class TestCalendarMapping(TestCase):
    def test_get_by_major(self):
        cals = get_calendars_for_majors(['TRAIN'])
        self.assertEqual(len(cals), 3)
        self.assertTrue('5_current' in cals[0])
        self.assertEqual(cals[0]['5_current'],
                         'http://art.washington.edu/calendar/')

    def test_get_by_minor(self):
        cals = get_calendars_for_minors(['TRAINR'])
        self.assertEqual(len(cals), 3)
        self.assertTrue('2_current' in cals[0])

        self.assertIsNone(cals[0]['2_current'])

    def test_get_by_gradmajor(self):
        cals = get_calendars_for_gradmajors(['UPCOM'])
        self.assertEqual(len(cals), 3)
        cal_ids = []
        for cal in cals:
            cal_ids = cal_ids + cal.keys()
        self.assertIn('future_1', cal_ids)
        self.assertIn('far_future', cal_ids)
        self.assertIn('past', cal_ids)

    def test_no_calendar(self):
        cals = get_calendars_for_gradmajors(['TRAINS'])
        self.assertEqual(len(cals), 0)

    def test_unknown_major(self):
        cals = get_calendars_for_gradmajors(['WTFBBQ'])
        self.assertEqual(len(cals), 0)

    def test_dupe_calendar(self):
        major_cals = get_calendars_for_majors(['TRAIN'])
        minor_cals = get_calendars_for_minors(['TRAINR'])
        cals = major_cals + minor_cals
        self.assertEqual(len(cals), 5)
