# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from unittest.mock import patch
import json
from myuw.dao.pds import (
    get_pds_data, get_cache_key, clear_cached_data, get_cached_data,
    process_record)
from myuw.test import get_request_with_user, fdao_pws_override

DATA = json.dumps({
    "application_status_code": "1",
    "total_deductible_credits": "0.0",
    "total_extension_credits": "0.0",
    "total_grade_attempted": "40.0",
    "total_lower_div_transfer_credits": "84.0",
    "total_upper_div_transfer_credits": "0.0",
    "total_non_graded_credits": "3.0",
    "last_enrolled_term": {"year": 2023, "quarter": 2},
    "terms_completed": [
        {"year": 2012, "quarter": 4},
        {"year": 2013, "quarter": 1},
        {"year": 2013, "quarter": 2}],
})


@fdao_pws_override
class TestPwsDao(TestCase):

    def test_get_cache_key(self):
        self.assertEqual(
            get_cache_key(1),
            "person_data_store/application_type_credits_transcript_terms/1")

    def test_clear_cached_data(self):
        with patch('myuw.dao.pds.cache_client.delete') as mock:
            mock.return_value = True
            self.assertTrue(clear_cached_data(1))

    def test_get_cached_data(self):
        with patch('myuw.dao.pds.cache_client.get') as mock:
            mock.return_value = DATA
            self.assertEqual(get_cached_data(1), DATA)

    def test_get_pds_data(self):
        req = get_request_with_user('javerage')
        with patch('myuw.dao.pds.get_cached_data') as mock:
            mock.return_value = DATA
            self.assertEqual(
                get_pds_data(req),
                {
                    "is_transfer": False,
                    "total_credit": 127.0,
                    "completed_terms": 3
                }
            )
