# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.templatetags.hashing_tag import hash_netid
from myuw.templatetags.myuw_large_number_display import large_number


class TestNetidHash(TestCase):
    def test_netids(self):
        self.assertEqual(hash_netid('javerage'),
                         'c13c917a1822a8acd58c48d2c8c6880a')
        self.assertEqual(hash_netid('eight'),
                         '24d27c169c2c881eb09a065116f2aa5c')
        self.assertEqual(hash_netid('none'),
                         '334c4a4c42fdb79d7ebc3e73b517e6f8')


class TestLargeNumberDisplay(TestCase):
    def test_numbers(self):
        self.assertEqual(999, large_number(999))
        self.assertEqual('1K', large_number(1000))
        self.assertEqual('1K', large_number(1900))
        self.assertEqual('27K', large_number(27900))
        self.assertEqual('4M', large_number(4000000))
        self.assertEqual('3B', large_number(3000000000))
