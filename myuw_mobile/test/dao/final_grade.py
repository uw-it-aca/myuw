from django.test import TestCase
from myuw_mobile.dao.final_grade import _get_grades_by_regid_and_term
from restclients.models import Term


class TestFinalGrade(TestCase):

    def test_get_by_term(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2013
        term.quarter = "summer"

        grades = _get_grades_by_regid_and_term(regid, term)

        self.assertEquals(len(grades), 5)
        self.assertEquals(grades['2013,summer,TRAIN,101/A'].grade, 'CR')
        self.assertEquals(grades['2013,summer,PHYS,121/A'].grade, '3.1')

        self.assertEquals(_get_grades_by_regid_and_term(None, term), None)
        self.assertEquals(_get_grades_by_regid_and_term("123asd", term), None)
