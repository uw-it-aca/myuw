from unittest2 import TestCase
from uw_sws.enrollment import enrollment_search_by_regid
from uw_sws.models import Term

from myuw.dao.pws import get_regid_of_current_user
from myuw.dao.student import get_class_standings, get_majors, \
    get_student_status, get_rollup_and_future_majors, get_minors, \
    get_rollup_and_future_minors, _get_minors, _get_majors, _get_class_standings
from myuw.test import get_request_with_date, get_request_with_user

javerage_regid = '9136CCB8F66711D5BE060004AC494FFE'
test_regid = '9136CCB8F66711D5BE060024ACA9CFDE'
testalicious_regid = '9136CCB8F66711D5BE060024ACA9CFAE'

winter_2013 = Term()
winter_2013.year = 2013
winter_2013.quarter = Term.WINTER

spring_2013 = Term()
spring_2013.year = 2013
spring_2013.quarter = Term.SPRING

summer_2013 = Term()
summer_2013.year = 2013
summer_2013.quarter = Term.SUMMER

autumn_2013 = Term()
autumn_2013.year = 2013
autumn_2013.quarter = Term.AUTUMN

winter_2014 = Term()
winter_2014.year = 2014
winter_2014.quarter = Term.WINTER


class TestStudentDAO(TestCase):

    def setUp(self):
        self.javerage_req = get_request_with_user('javerage',
                                                  get_request_with_date("2013-04-10"))

    def get_majors(self, regid):
        enrollments = enrollment_search_by_regid(regid)
        return _get_majors(enrollments)

    def get_minors(self, regid):
        enrollments = enrollment_search_by_regid(regid)
        return _get_minors(enrollments)

    def get_class_standing(self, regid):
        enrollments = enrollment_search_by_regid(regid)
        return _get_class_standings(enrollments)

    def test_get_majors(self):
        majors = self.get_majors(test_regid)

        self.assertNotIn('current', majors)

        self.assertEquals(majors['rollup'][0].full_name,
                          "Test Major")

        majors = get_majors(self.javerage_req)

        self.assertIn("majors", majors)
        self.assertIn("current", majors)
        self.assertIn("rollup", majors)

        self.assertEquals(majors['current'][0].full_name,
                          "App & Comp Math Sci (Social & Behav Sci)")

        self.assertEquals(majors['rollup'][0].full_name,
                          "App & Comp Math Sci (Social & Behav Sci)")

        term_majors = majors['majors']

        self.assertEquals(term_majors[spring_2013][0].full_name,
                          "App & Comp Math Sci (Social & Behav Sci)")

        self.assertEquals(term_majors[autumn_2013][0].full_name,
                          "Computer Science")

        self.assertEquals(term_majors[winter_2014][0].full_name,
                          "English")

        majors = self.get_majors(testalicious_regid)

        self.assertEquals(majors['rollup'][0].full_name,
                          "App & Comp Math Sci (Social & Behav Sci)")

    def test_get_class_standing(self):
        class_standings = get_class_standings(self.javerage_req)

        self.assertIn("class_level", class_standings)
        self.assertIn("current", class_standings)
        self.assertIn("rollup", class_standings)

    def test_get_student_status(self):
        student_status = get_student_status(self.javerage_req)

        self.assertIn("majors", student_status)
        self.assertIn("class_level", student_status)

    def test_get_minors(self):
        minors = self.get_minors(test_regid)

        self.assertNotIn('current', minors)

        self.assertEquals(minors['rollup'][0].full_name,
                          "American Sign Language")

        minors = get_minors(self.javerage_req)

        self.assertIn("minors", minors)
        self.assertIn("current", minors)
        self.assertIn("rollup", minors)

        self.assertEquals(minors['current'][0].full_name,
                          "American Sign Language")

        self.assertEquals(minors['rollup'][0].full_name,
                          "American Sign Language")

        term_minors = minors['minors']

        self.assertEquals(term_minors[spring_2013][0].full_name,
                          "American Sign Language")

        self.assertEquals(term_minors[autumn_2013][0].full_name,
                          "American Sign Language")

        self.assertEquals(term_minors[winter_2014][0].full_name,
                          "Mathematics")

        minors = self.get_minors(testalicious_regid)

        self.assertEquals(minors['rollup'][0].full_name,
                          "American Sign Language")

    def test_get_rollup_and_future(self):

        majors = get_majors(self.javerage_req)

        future_rollup_majors = get_rollup_and_future_majors(majors)

        intended_majors = [u'ENGLISH', u'ACMS (SOC & BEH SCI)',
                           u'COMPUTER SCIENCE']

        intended_minors = [u'MATH', u'ASL']

        minors = get_minors(self.javerage_req)

        future_rollup_minors = get_rollup_and_future_minors(minors)

        for major in future_rollup_majors:
            self.assertIn(major.major_name, intended_majors)

        for minor in future_rollup_minors:
            self.assertIn(minor.short_name, intended_minors)
