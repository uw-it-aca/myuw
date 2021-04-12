# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.conf import settings
from restclients_core.exceptions import DataFailureException
from uw_sws.section import get_section_by_label
from uw_sws.registration import get_schedule_by_regid_and_term
from uw_sws.term import get_term_by_date, get_specific_term
from myuw.dao.registration import (
    get_schedule_by_term, _get_current_summer_term, _is_split_summer)
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_user, get_request_with_date


@fdao_pws_override
@fdao_sws_override
class TestRegistrationsDao(TestCase):

    def test_not_registered_or_error(self):
        request = get_request_with_user(
            'javerage', get_request_with_date("2014-10-01"))
        # normally get_schedule_by_term wouldn't return
        # DataFailureException Status code: 404.
        self.assertRaises(DataFailureException, get_schedule_by_term, request)

        request = get_request_with_user('jinter')
        schedule = get_schedule_by_term(request)
        self.assertEqual(len(schedule.sections), 0)

    def test_get_current_summer_term(self):
        schedule = get_schedule_by_regid_and_term(
            "9136CCB8F66711D5BE060004AC494FFE",
            get_specific_term(2013, 'summer'))
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-06-24"))
        for sterm in ['A-term', 'B-term', 'Full-term']:
            self.assertEqual(_get_current_summer_term(
                request, schedule, sterm), sterm.lower())

        self.assertEqual(
            _get_current_summer_term(request, schedule, None), 'a-term')

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-07-24"))
        self.assertEqual(
            _get_current_summer_term(request, schedule, None), 'a-term')

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-07-25"))
        self.assertEqual(
            _get_current_summer_term(request, schedule, None), 'b-term')

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-08-28"))
        self.assertEqual(_get_current_summer_term(request, schedule, None),
                         'full-term')

    def test_get_schedule_by_term(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-10-01"))
        schedule = get_schedule_by_term(request)
        self.assertEqual(len(schedule.sections), 2)
        self.assertEqual(schedule.sections[0].color_id, 1)
        self.assertEqual(schedule.sections[1].color_id, 2)

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-04-01"))
        schedule = get_schedule_by_term(request)
        self.assertEqual(len(schedule.sections), 5)
        self.assertEqual(schedule.sections[0].color_id, 1)
        self.assertEqual(schedule.sections[1].color_id, 2)
        self.assertEqual(schedule.sections[2].color_id, 3)
        self.assertEqual(schedule.sections[3].color_id, '3a')
        self.assertEqual(schedule.sections[4].color_id, '3a')

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-06-24"))
        schedule = get_schedule_by_term(request)
        self.assertEqual(schedule.summer_term, "a-term")
        self.assertEqual(len(schedule.sections), 2)

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-07-24"))
        schedule = get_schedule_by_term(request)
        self.assertEqual(schedule.summer_term, "a-term")
        self.assertEqual(schedule.registered_summer_terms,
                         {'a-term': True, 'b-term': False, 'full-term': True})
        self.assertEqual(len(schedule.sections), 2)
        self.assertEqual(schedule.sections[0].summer_term, "A-term")
        self.assertEqual(schedule.sections[0].color_id, 1)
        self.assertEqual(schedule.sections[1].summer_term, "Full-term")
        self.assertEqual(schedule.sections[1].color_id, 2)

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-07-25"))
        schedule = get_schedule_by_term(request)
        self.assertEqual(schedule.summer_term, "b-term")
        self.assertEqual(len(schedule.sections), 2)
        self.assertEqual(schedule.sections[0].summer_term, "B-term")
        self.assertEqual(schedule.sections[1].summer_term, "Full-term")

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-07-25"))
        schedule = get_schedule_by_term(
            request, term=get_specific_term(2013, 'summer'),
            summer_term="full-term")
        self.assertEqual(schedule.summer_term, "full-term")
        self.assertEqual(len(schedule.sections), 3)
        self.assertEqual(schedule.sections[0].summer_term, "A-term")
        self.assertEqual(schedule.sections[1].summer_term, "B-term")
        self.assertEqual(schedule.sections[2].summer_term, "Full-term")

        request = get_request_with_user('jeos',
                                        get_request_with_date("2013-07-24"))
        schedule = get_schedule_by_term(request)
        self.assertEqual(schedule.registered_summer_terms, {'b-term': False})
        self.assertEqual(len(schedule.sections), 0)
        self.assertEqual(schedule.summer_term, "a-term")

        request = get_request_with_user('jeos',
                                        get_request_with_date("2013-07-25"))
        schedule = get_schedule_by_term(request)
        self.assertEqual(schedule.summer_term, "b-term")
        self.assertEqual(schedule.registered_summer_terms, {'b-term': True})
        self.assertEqual(len(schedule.sections), 1)
        self.assertEqual(str(schedule.sections[0].start_date), "2013-07-22")
        self.assertEqual(str(schedule.sections[0].end_date), "2013-09-06")
        self.assertEqual(schedule.sections[0].section_label(),
                         "2013,summer,LIS,498/C")

        request = get_request_with_user('eight')
        schedule = get_schedule_by_term(request)
        self.assertEqual(len(schedule.sections), 8)

        request = get_request_with_user('eight',
                                        get_request_with_date("2013-07-25"))
        schedule = get_schedule_by_term(request)
        self.assertEqual(schedule.registered_summer_terms,
                         {'a-term': False, 'b-term': True, 'full-term': True})
        self.assertEqual(schedule.summer_term, "b-term")
        self.assertEqual(len(schedule.sections), 2)

    def test_future_term_schedule(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-06-01"))
        schedule = get_schedule_by_term(
            request, term=get_specific_term(2013, 'autumn'))
        self.assertEqual(len(schedule.sections), 2)

        schedule = get_schedule_by_term(
            request, term=get_specific_term(2013, 'summer'),
            summer_term='A-term')
        self.assertEqual(len(schedule.sections), 2)
        self.assertEqual(schedule.summer_term, "a-term")

    def test_tsprint_false_instructor(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2014-01-01"))
        schedule = get_schedule_by_term(request)
        self.assertEqual(len(schedule.sections), 5)

        PHYS_122_a = schedule.sections[2]
        self.assertEqual(PHYS_122_a.section_label(),
                         "2014,winter,PHYS,122/A")
        self.assertEqual(len(PHYS_122_a.meetings), 2)

        meeting0_instructors = PHYS_122_a.meetings[0].instructors
        self.assertEqual(len(meeting0_instructors), 2)
        self.assertEqual(meeting0_instructors[0].display_name,
                         "SEATTLE GRADUATE STUDENT")
        self.assertEqual(meeting0_instructors[1].display_name,
                         "J. Average Student")

        meeting1_instructors = PHYS_122_a.meetings[1].instructors
        self.assertEqual(len(meeting1_instructors), 2)
        self.assertEqual(meeting1_instructors[0].display_name,
                         "SEATTLE GRADUATE STUDENT")
        self.assertEqual(meeting1_instructors[1].display_name,
                         "Seattle Faculty")

    def test_remote_section(self):
        request = get_request_with_user('eight',
                                        get_request_with_date("2020-10-01"))
        schedule = get_schedule_by_term(request)
        self.assertIsNotNone(schedule)
        self.assertEqual(len(schedule.sections), 3)
        self.assertTrue(schedule.sections[0].is_remote)

    def test_is_split_summer(self):
        self.assertTrue(_is_split_summer({'a-term': True}))
        self.assertTrue(_is_split_summer({'b-term': True}))
        self.assertTrue(_is_split_summer({'a-term': True,
                                          'b-term': True}))
        self.assertTrue(_is_split_summer({'a-term': True,
                                          'full-term': True}))
        self.assertTrue(_is_split_summer({'b-term': True,
                                          'full-term': True}))
        self.assertTrue(_is_split_summer({'a-term': True,
                                          'b-term': True,
                                          'full-term': True}))
        self.assertFalse(_is_split_summer({'full-term': True}))
