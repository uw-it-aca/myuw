from django.test import TestCase
from django.conf import settings
from restclients.sws.person import get_person_by_regid


class TestEightData(TestCase):
    """
    Ensuring that MYUW's mock data matches the spec defined here:
    https://docs.google.com/a/uw.edu/spreadsheets/d/1ZTC5FwvJQ9wqf8KLfBxIPOJPvp4aV-H1HvQ1jPqqh7E/edit#gid=0
    """

    def test_sws_person(self):
        with self.settings(
            RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File',
            RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            regid = "12345678901234567890123456789012"
            person = get_person_by_regid(regid)

            self.assertFalse(person.directory_release)
            self.assertEquals(person.first_name, "Evelyn Marie")
            self.assertEquals(person.last_name, "Hightower")
            self.assertEquals(person.employee_id, "87654321")
            self.assertEquals(person.student_number, "1443336")
            self.assertEquals(person.permanent_address.street_line1, "2032 S 320th St")
            self.assertEquals(person.permanent_address.city, "Federal Way")
            self.assertEquals(person.permanent_address.state, "WA")
            self.assertEquals(person.permanent_address.zip_code, "98003")

            self.assertEquals(person.local_address.street_line1, "1101 Pacific Ave S")
            self.assertEquals(person.local_address.street_line2, "#307")
            self.assertEquals(person.local_address.city, "Tacoma")
            self.assertEquals(person.local_address.state, "WA")
            self.assertEquals(person.local_address.zip_code, "98424")
            self.assertEquals(person.permanent_phone, "2535552468")
            self.assertIsNone(person.local_phone)
            self.assertEquals(person.email, "eight@u.washington.edu")
            self.assertIsNone(person.visa_type)


