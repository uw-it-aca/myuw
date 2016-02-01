from django.test import TestCase
from myuw.userservice_validation import validate, validate_shib, transform


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

    def test_shib_validation(self):
        invalid_string = ("Username not a valid netid (starts with a letter, "
                          "then 0-7 letters or numbers)")
        self.assertEquals(validate_shib("javerage"), invalid_string)
        self.assertEquals(validate_shib("javerage@washington.edu"), None)

    def test_transform(self):
        self.assertEquals(transform("JAVERAGE"), "javerage@washington.edu")
        self.assertEquals(transform("javerage@washington.edu"),
                          "javerage@washington.edu")
        self.assertEquals(transform("javerage@gmail.com"),
                          "javerage@gmail.com")
