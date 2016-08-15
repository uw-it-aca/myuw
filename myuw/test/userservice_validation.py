from django.test import TestCase
from myuw.userservice_validation import validate, INVALID_STRING,\
    UPPERCASE, NO_USER


class TestValidation(TestCase):

    def test_validation(self):
        self.assertEquals(validate("javerage"), None)
        self.assertEquals(validate(""), NO_USER)
        self.assertEquals(validate("JaVeRaGe"), UPPERCASE)
        self.assertEquals(validate("a_canvas"), None)
        self.assertEquals(validate("99invalid"), INVALID_STRING)
        self.assertEquals(validate("thisisfartoolongtobeanetid"),
                          INVALID_STRING)
