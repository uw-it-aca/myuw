import json
from unittest.mock import patch, mock_open

from django.core.cache import cache
from django.test import TestCase, override_settings

from myuw.templatetags.hashing_tag import hash_netid
from myuw.templatetags.myuw_large_number_display import large_number


class TestNetidHash(TestCase):
    def test_netids(self):
        self.assertEquals(hash_netid('javerage'),
                          'c13c917a1822a8acd58c48d2c8c6880a')
        self.assertEquals(hash_netid('eight'),
                          '24d27c169c2c881eb09a065116f2aa5c')
        self.assertEquals(hash_netid('none'),
                          '334c4a4c42fdb79d7ebc3e73b517e6f8')


class TestLargeNumberDisplay(TestCase):
    def test_numbers(self):
        self.assertEquals(999, large_number(999))
        self.assertEquals('1K', large_number(1000))
        self.assertEquals('1K', large_number(1900))
        self.assertEquals('27K', large_number(27900))
        self.assertEquals('4M', large_number(4000000))
        self.assertEquals('3B', large_number(3000000000))
