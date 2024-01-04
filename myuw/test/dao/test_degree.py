# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.degree import get_degrees, get_degrees_json
from myuw.test import get_request_with_date, get_request_with_user

DEGREE_DATA = {
    'degrees': [{
        'after_last_final_exam_day': False,
        'campus': 'SEATTLE',
        'diploma_mail': 0,
        'diploma_mail_to_local_address': False,
        'has_applied': True,
        'is_admin_hold': False,
        'is_granted': False,
        'is_incomplete': False,
        'is_degree_earned_term': False,
        'before_degree_earned_term': True,
        'during_april_may': True,
        "last_4_inst_weeks_in_degree_term": False,
        'level': 1,
        'name_on_diploma': 'John Joseph Average',
        'quarter': 'summer',
        'status': 5,
        'title': 'BACHELOR OF ARTS (POLITICAL SCIENCE)',
        'type': 1,
        'year': 2013}],
    'error_code': None}


class TestAdviserDao(TestCase):

    def test_get_degrees(self):
        degrees = get_degrees(
            get_request_with_user('javerage')
        )
        self.assertEquals(len(degrees), 1)

        degrees = get_degrees(
            get_request_with_user('eight')
        )
        self.assertEquals(len(degrees), 2)

        self.assertRaises(DataFailureException,
                          get_degrees,
                          get_request_with_user('jerror'))

        self.assertRaises(DataFailureException,
                          get_degrees,
                          get_request_with_user('jinter'))

    def test_get_degrees_json(self):
        degree_data = get_degrees_json(
            get_request_with_user('javerage')
        )
        self.maxDiff = None
        self.assertEquals(degree_data, DEGREE_DATA)
        self.maxDiff = None
        degree_data = get_degrees_json(
            get_request_with_user('eight', get_request_with_date("2013-05-10"))
        )
        self.assertEquals(
            degree_data,
            {
                'degrees': [
                    {
                        'before_degree_earned_term': False,
                        'campus': 'TACOMA',
                        'diploma_mail': 0,
                        'diploma_mail_to_local_address': False,
                        'during_april_may': True,
                        'has_applied': False,
                        'is_admin_hold': False,
                        'is_degree_earned_term': True,
                        'is_granted': False,
                        'is_incomplete': True,
                        'level': 1,
                        'name_on_diploma': 'Eight Student',
                        'quarter': 'spring',
                        'status': 2,
                        'title': 'BACHELOR OF ARTS IN BUSINESS ADMINISTRATION',
                        'type': 1,
                        'year': 2013
                    },
                    {
                        'before_degree_earned_term': False,
                        'campus': 'TACOMA',
                        'diploma_mail': 0,
                        'diploma_mail_to_local_address': False,
                        'during_april_may': True,
                        'has_applied': False,
                        'is_admin_hold': False,
                        'is_degree_earned_term': True,
                        'is_granted': True,
                        'is_incomplete': False,
                        'level': 1,
                        'name_on_diploma': 'Eight Student',
                        'quarter': 'spring',
                        'status': 9,
                        'title': 'BACHELOR OF SCIENCE IN DATA SCIENCE',
                        'type': 6,
                        'within_2terms_after_granted': True,
                        'year': 2013
                    }
                    ],
                'error_code': None
            })

        degree_data = get_degrees_json(
            get_request_with_user(
                'javerage', get_request_with_date("2013-07-26"))
        )
        self.assertFalse(
            degree_data['degrees'][0]['last_4_inst_weeks_in_degree_term'])
        degree_data = get_degrees_json(
            get_request_with_user(
                'javerage', get_request_with_date("2013-07-27"))
        )
        self.assertTrue(
            degree_data['degrees'][0]['last_4_inst_weeks_in_degree_term'])

        degree_data = get_degrees_json(
            get_request_with_user('jbothell')
        )
        self.assertEquals(
            degree_data,
            {'degrees': None, 'error_code': 404})

        # MUWM-5232
        degree_data = get_degrees_json(
            get_request_with_user(
                'javerage', get_request_with_date("2013-08-22")))
        self.assertFalse(
            degree_data['degrees'][0]['after_last_final_exam_day'])
        degree_data = get_degrees_json(
            get_request_with_user(
                'javerage', get_request_with_date("2013-08-23")))
        self.assertTrue(
            degree_data['degrees'][0]['after_last_final_exam_day'])
        degree_data = get_degrees_json(
            get_request_with_user(
                'javerage', get_request_with_date("2013-09-19")))
        self.assertTrue(
            degree_data['degrees'][0]['after_last_final_exam_day'])
