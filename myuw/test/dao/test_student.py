from unittest2 import TestCase
from uw_sws.models import Term

from myuw.dao.student import get_class_standings, get_majors

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

    def test_get_majors(self):
        majors = get_majors(javerage_regid)

        self.assertIn("standings", majors)
        self.assertIn("current", majors)
        self.assertIn("rollup", majors)

        self.assertEquals(majors['current']['FullName'],
                          "App & Comp Math Sci (Social & Behav Sci)")

        self.assertEquals(majors['rollup']['FullName'],
                          "App & Comp Math Sci (Social & Behav Sci)")

        term_majors = majors['majors']

        self.assertEquals(term_majors[spring_2013]['FullName'],
                          "App & Comp Math Sci (Social & Behav Sci)")

        self.assertEquals(term_majors[autumn_2013]['FullName'],
                          "American Sign Language")

        self.assertEquals(term_majors[winter_2014]['FullName'],
                          "English")

        majors = get_majors(test_regid)

        self.assertNotIn('current', majors)

        self.assertEquals(majors['rollup']['FullName'],
                          "App & Comp Math Sci (Social & Behav Sci)")

    def test_get_class_standing(self):

        class_standings = get_class_standings(javerage_regid)

        self.assertIn(class_standings, "standings")
        self.assertIn(class_standings, "current")
        self.assertIn(class_standings, "rollup")

    def test_get_student_status(self):
        pass
