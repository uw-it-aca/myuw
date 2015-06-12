from django.test import TestCase
import datetime
from myuw_mobile.dao.library import _get_account_by_uwnetid
from myuw_mobile.dao.library import get_subject_guide_by_section
from myuw_mobile.dao.schedule import _get_schedule
from restclients.models.sws import Term, Section


FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_PWS = 'restclients.dao_implementation.pws.File'


class TestLibrary(TestCase):

    def test_get_account_balance(self):
        self.assertEquals(_get_account_by_uwnetid(None), None)

        javerage_acct = _get_account_by_uwnetid('javerage')
        self.assertEquals(javerage_acct.next_due, datetime.date(2014, 5, 27))

        self.assertEquals(_get_account_by_uwnetid("123notarealuser"), None)

    def test_get_subject_guide_by_section(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):
            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term = Term()
            term.year = 2013
            term.quarter = "spring"
            schedule = _get_schedule(regid, term)
            for section in schedule.sections:
                if section.curriculum_abbr == 'TRAIN':
                    self.assertEquals(
                        get_subject_guide_by_section(section),
                        "http://www.lib.washington.edu/subject/")
                if section.curriculum_abbr == 'PHYS':
                    self.assertEquals(
                        get_subject_guide_by_section(section),
                        "http://guides.lib.washington.edu/physics_astronomy")
