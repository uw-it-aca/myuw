# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.dao.student_profile import (
    _get_degrees_for_terms, get_degree_status,
    get_cur_future_enrollments, get_student_profile)
from myuw.test import (
    fdao_sws_override, fdao_pws_override,
    get_request_with_date, get_request_with_user)
from myuw.test.dao.test_degree import DEGREE_DATA


@fdao_pws_override
@fdao_sws_override
class TestStudentProfile(TestCase):
    def test_get_majors_for_terms(self):
        req = get_request_with_user('eight',
                                    get_request_with_date("2013-04-01"))
        terms, enrollments = get_cur_future_enrollments(req)
        majors = _get_degrees_for_terms(terms, enrollments, "majors")

        self.assertEquals(len(majors[0]['majors']), 2)
        self.assertEquals(len(majors[1]['majors']), 3)
        self.assertEquals(len(majors[2]['majors']), 2)

        req = get_request_with_user('eight',
                                    get_request_with_date("2016-04-01"))
        self.assertIsNone(get_cur_future_enrollments(req))

    def test_get_minors_for_terms(self):
        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-04-01"))
        terms, enrollments = get_cur_future_enrollments(req)
        minors = _get_degrees_for_terms(terms, enrollments, "minors")

        self.assertEquals(len(minors[0]['minors']), 1)
        self.assertEquals(len(minors[1]['minors']), 2)

    def test_major_no_change(self):
        req = get_request_with_user('javg005',
                                    get_request_with_date("2013-04-01"))
        terms, enrollments = get_cur_future_enrollments(req)

        majors = _get_degrees_for_terms(terms, enrollments, "majors")
        minors = _get_degrees_for_terms(terms, enrollments, "minors")

        for major in majors:
            self.assertFalse(major['degrees_modified'])

        for minor in minors:
            self.assertFalse(minor['degrees_modified'])

    def test_major_drop_empty(self):
        req = get_request_with_user('jeos',
                                    get_request_with_date("2013-01-10"))
        terms, enrollments = get_cur_future_enrollments(req)
        majors = _get_degrees_for_terms(terms, enrollments, "majors")
        minors = _get_degrees_for_terms(terms, enrollments, "minors")
        self.assertEquals(len(minors), 4)
        for minor in minors:
            self.assertFalse(minor['degrees_modified'])
            self.assertEquals(len(minor["minors"]), 0)

        self.assertEquals(len(majors), 4)
        self.assertFalse(majors[0]['degrees_modified'])
        self.assertTrue(len(majors[0]["majors"]) > 0)

        self.assertTrue(majors[1]['degrees_modified'])
        self.assertTrue(len(majors[1]["majors"]) == 0)
        self.assertTrue(majors[1]['has_only_dropped'])

        self.assertFalse(majors[2]['degrees_modified'])
        self.assertTrue(len(majors[2]["majors"]) == 0)
        self.assertFalse(majors[2]['has_only_dropped'])

        self.assertFalse(majors[3]['degrees_modified'])
        self.assertTrue(len(majors[3]["majors"]) == 0)
        self.assertFalse(majors[3]['has_only_dropped'])

    def test_class_standing(self):
        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-07-01"))
        data = get_student_profile(req)
        self.assertEqual(data['class_level'], 'SOPHOMORE')

    def test_degree_status(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-01"))
        data = get_student_profile(req)
        self.assertEqual(data['degree_status'], DEGREE_DATA)

        # enrolled in the previous term
        req = get_request_with_user('javg003',
                                    get_request_with_date("2013-07-01"))
        self.assertEqual(data['degree_status'], DEGREE_DATA)

        # enrolled in the term before previous term
        req = get_request_with_user('javg003',
                                    get_request_with_date("2013-10-01"))
        self.assertEqual(data['degree_status'], DEGREE_DATA)

        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-04-01"))
        data = get_student_profile(req)
        self.assertIsNone(data['degree_status'])

    def test_residency_status_change(self):
        req = get_request_with_user('javg002',
                                    get_request_with_date("2013-04-01"))
        data = get_student_profile(req)
        self.assertTrue(data['has_pending_residency_change'])
        self.assertEqual(
            data['pending_residency_change_term'],
            {"year": 2013, "quarter": "autumn"})
