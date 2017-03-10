import datetime
from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.library import _get_account_by_uwnetid
from myuw.dao.library import get_subject_guide_by_section
from myuw.dao.schedule import _get_schedule
from uw_sws.models import Term
from myuw.test import fdao_pws_override, fdao_sws_override, get_request


@fdao_pws_override
@fdao_sws_override
class TestLibrary(TestCase):

    def setUp(self):
        get_request()

    def test_get_account_balance(self):
        self.assertEquals(_get_account_by_uwnetid(None), None)

        javerage_acct = _get_account_by_uwnetid('javerage')
        self.assertEquals(javerage_acct.next_due, datetime.date(2014, 5, 27))

        self.assertRaises(DataFailureException,
                          _get_account_by_uwnetid,
                          "123notarealuser")

    def test_get_subject_guide_bothell(self):
        regid = "FE36CCB8F66711D5BE060004AC494FCD"
        term = Term()
        term.year = 2013
        term.quarter = "spring"
        schedule = _get_schedule(regid, term)
        for section in schedule.sections:
            # has subject guide link
            if section.curriculum_abbr == 'BISSEB' and\
                    section.course_number == '259':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/bothell/businternational")
            # 404, general guide link
            if section.curriculum_abbr == 'BCWRIT' and\
                    section.course_number == '500':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/bothell/")

    def test_get_subject_guide_seattle(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2013
        term.quarter = "spring"
        schedule = _get_schedule(regid, term)
        for section in schedule.sections:
            # 404, general guide link
            if section.curriculum_abbr == 'TRAIN' and\
                    section.course_number == '101':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/research")

            # has subject guide link
            if section.curriculum_abbr == 'TRAIN' and\
                    section.course_number == '100':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/friendly.php?s=research/pnw")

            # has subject guide link
            if section.curriculum_abbr == 'PHYS' and\
                    section.course_number == '121':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "%s?%s" % ("http://guides.lib.uw.edu/friendly.php",
                               "s=research/physics_astronomy"))

    def test_get_subject_guide_tacoma(self):
        regid = "12345678901234567890123456789012"
        term = Term()
        term.year = 2013
        term.quarter = "spring"
        schedule = _get_schedule(regid, term)
        for section in schedule.sections:
            # 404, general guide link
            if section.curriculum_abbr == 'ROLING' and\
                    section.course_number == '310':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/tacoma")

            if section.curriculum_abbr == 'T ARTS' and\
                    section.course_number == '110':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/tacoma")

            # has subject guide link
            if section.curriculum_abbr == 'ARCTIC' and\
                    section.course_number == '200':
                self.assertEquals(
                    get_subject_guide_by_section(section),
                    "http://guides.lib.uw.edu/tacoma/art")
