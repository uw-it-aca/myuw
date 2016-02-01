from django.test import TestCase
from myuw.dao.pws import descope_uw_username


class TestPWS(TestCase):
    def test_descope_uw(self):
        self.assertEquals(descope_uw_username("javerage"), "javerage")
        self.assertEquals(descope_uw_username("javerage@washington.edu"),
                          "javerage")
        self.assertEquals(descope_uw_username("javerage@gmail.com"),
                          "javerage@gmail.com")
