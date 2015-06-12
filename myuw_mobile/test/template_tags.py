from django.test import TestCase
from myuw_mobile.templatetags.hashing_tag import hash_netid


class TestNetidHash(TestCase):
    def test_netids(self):
        self.assertEquals(hash_netid('javerage'),
                          'c13c917a1822a8acd58c48d2c8c6880a')
        self.assertEquals(hash_netid('eight'),
                          '24d27c169c2c881eb09a065116f2aa5c')
        self.assertEquals(hash_netid('none'),
                          '334c4a4c42fdb79d7ebc3e73b517e6f8')
