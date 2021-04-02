# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime
from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.library import _get_account_by_uwnetid
from myuw.dao.library import get_subject_guide_by_section
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.term import get_current_quarter
from myuw.test import fdao_pws_override, fdao_sws_override,\
    get_request_with_user, get_request_with_date


@fdao_pws_override
@fdao_sws_override
class TestLibrary(TestCase):

    def test_get_account_balance(self):
        self.assertEquals(_get_account_by_uwnetid(None), None)

        javerage_acct = _get_account_by_uwnetid('javerage')
        self.assertEquals(str(javerage_acct.next_due),
                          '2014-05-27 02:00:00+00:00')

        self.assertRaises(DataFailureException,
                          _get_account_by_uwnetid,
                          "123notarealuser")

    def test_get_subject_guide_bothell(self):
        req = get_request_with_user('jbothell',
                                    get_request_with_date("2013-04-01"))
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)
        for section in schedule.sections:
            # has subject guide link
            if section.curriculum_abbr == 'BISSEB' and\
                    section.course_number == '259':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/bothell/businternational")
            # 404, general guide link
            if section.curriculum_abbr == 'BCWRIT' and\
                    section.course_number == '500':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/bothell/")

    def test_get_subject_guide_seattle(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-01"))
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)
        for section in schedule.sections:
            # 404, general guide link
            if section.curriculum_abbr == 'TRAIN' and\
                    section.course_number == '101':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/research")

            # has subject guide link
            if section.curriculum_abbr == 'TRAIN' and\
                    section.course_number == '100':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/friendly.php?s=research/pnw")

            # has subject guide link
            if (section.curriculum_abbr == 'PHYS' and
                    section.course_number == '121' and
                    section.section_id == 'A'):
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "{}?{}".format("http://guides.lib.uw.edu/friendly.php",
                                   "s=research/physics_astronomy"))

            if (section.curriculum_abbr == 'PHYS' and
                    section.course_number == '121' and
                    section.section_id == 'AQ'):
                self.assertRaises(DataFailureException,
                                  get_subject_guide_by_section,
                                  section)

    def test_get_subject_guide_tacoma(self):
        req = get_request_with_user('eight',
                                    get_request_with_date("2013-04-01"))
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)
        for section in schedule.sections:
            # 404, general guide link
            if section.curriculum_abbr == 'ROLING' and\
                    section.course_number == '310':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/tacoma")

            if section.curriculum_abbr == 'T ARTS' and\
                    section.course_number == '110':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/tacoma")

            # has subject guide link
            if section.curriculum_abbr == 'ARCTIC' and\
                    section.course_number == '200':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/tacoma/art")
