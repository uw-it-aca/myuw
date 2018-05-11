from django.test import TestCase
from myuw.userservice_validation import validate, INVALID_STRING, NO_USER,\
    can_override, is_admin


class TestValidation(TestCase):

    def test_validation(self):
        self.assertEquals(validate("javerage"), None)
        self.assertEquals(validate(""), NO_USER)
        self.assertEquals(validate("jaVeRaGe"), None)
        self.assertEquals(validate("a_canvas"), None)
        self.assertEquals(validate("99invalid"), INVALID_STRING)
        self.assertEquals(validate("thisisfartoolongtobeanetid"),
                          INVALID_STRING)
