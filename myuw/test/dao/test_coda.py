# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from unittest.mock import patch
from restclients_core.exceptions import DataFailureException
from myuw.dao import coda


class TestCoDaDAO(TestCase):

    def test_process_section_label(self):

        section_label = "2018_winter_T_UNIV_200_A"

        processed = coda._process_section_label(section_label)

        self.assertEquals("2018-winter-T%20UNIV-200-A", processed)

        section_label = "2018_winter_ES S_102_A"

        processed = coda._process_section_label(section_label)

        self.assertEquals("2018-winter-ES%20S-102-A", processed)

    @patch('myuw.dao.coda.get_fail_rate', spec=True)
    def test_get_fail_rate_err(self, mock):
        json_obj = {}
        mock.side_effect = UnicodeDecodeError
        coda._set_json_fail_rate("2018_winter_ES S_102_A", json_obj)

    @patch('myuw.dao.coda.get_course_cgpa', spec=True)
    def test_get_course_cgpa(self, mock):
        json_obj = {}
        mock.side_effect = DataFailureException(None, 500, "Code err")
        coda._set_json_cgpa("2018_winter_ES S_102_A", json_obj)
