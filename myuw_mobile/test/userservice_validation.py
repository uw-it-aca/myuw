from django.test import TestCase
from myuw_mobile.userservice_validation import validate


class TestValidation(TestCase):

    def test_validation(self):
        invalid_string = ("Username not a valid netid (starts with a letter, "
                          "then 0-7 letters or numbers)")

        self.assertEquals(validate("javerage"), None)
        self.assertEquals(validate(""), "No override user supplied")
        self.assertEquals(validate("JaVeRaGe"),
                          "Usernames must be all lowercase")
        self.assertEquals(validate("a_canvas"), invalid_string)
        self.assertEquals(validate("99invalid"), invalid_string)
        self.assertEquals(validate("thisisfartoolongtobeanetid"),
                          invalid_string)
