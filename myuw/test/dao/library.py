from django.test import TestCase
import datetime
from restclients.exceptions import DataFailureException
from myuw.dao.library import _get_account_by_uwnetid
from myuw.dao.library import get_subject_guide_by_section
from myuw.dao.schedule import _get_schedule
from restclients.models.sws import Term, Section


FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_PWS = 'restclients.dao_implementation.pws.File'


class TestLibrary(TestCase):

    def test_get_account_balance(self):
        self.assertEquals(_get_account_by_uwnetid(None), None)

        javerage_acct = _get_account_by_uwnetid('javerage')
        self.assertEquals(javerage_acct.next_due, datetime.date(2014, 5, 27))

        self.assertRaises(DataFailureException,
                          _get_account_by_uwnetid,
                          "123notarealuser")

    def test_get_subject_guide_by_section(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term = Term()
            term.year = 2013
            term.quarter = "spring"
            schedule = _get_schedule(regid, term)
            for section in schedule.sections:
                if section.curriculum_abbr == 'TRAIN' and\
                        section.course_number == '101':
                    self.assertEquals(
                        get_subject_guide_by_section(section),
                        "http://guides.lib.uw.edu/research")
                if section.curriculum_abbr == 'TRAIN' and\
                        section.course_number == '100':
                    self.assertEquals(
                        get_subject_guide_by_section(section),
                        "http://guides.lib.uw.edu/friendly.php?s=research/pnw")
                if section.curriculum_abbr == 'PHYS':
                    self.assertEquals(
                        get_subject_guide_by_section(section),
                        "%s?%s" % ("http://guides.lib.uw.edu/friendly.php",
                                   "s=research/physics_astronomy"))

    def test_get_subject_guide_by_section(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            regid = "12345678901234567890123456789012"
            term = Term()
            term.year = 2013
            term.quarter = "spring"
            schedule = _get_schedule(regid, term)
            for section in schedule.sections:
                if section.curriculum_abbr == 'ROLING' and\
                        section.course_number == '310':
                    self.assertEquals(
                        get_subject_guide_by_section(section),
                        "http://guides.lib.uw.edu/tacoma")

    def test_get_subject_guide_by_section(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            regid = "FE36CCB8F66711D5BE060004AC494FCD"
            term = Term()
            term.year = 2013
            term.quarter = "spring"
            schedule = _get_schedule(regid, term)
            for section in schedule.sections:
                if section.curriculum_abbr == 'BISSEB' and\
                        section.course_number == '259':
                    self.assertEquals(
                        get_subject_guide_by_section(section),
                        "http://guides.lib.uw.edu/bothell/businternational")
                if section.curriculum_abbr == 'BCWRIT' and\
                        section.course_number == '500':
                    self.assertEquals(
                        get_subject_guide_by_section(section),
                        "http://guides.lib.uw.edu/bothell/")
