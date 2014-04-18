from django.test import TestCase
from myuw_mobile.dao.notice import NOTICE_CATEGORIES, UNKNOWN_CATEGORY_NAME, _get_notices_by_regid

class TestNotce(TestCase):

    def test_notice_category_uniqueness(self):
        combo, cat = zip(*NOTICE_CATEGORIES)
        self.assertEquals(len(combo), len(set(combo)))

    def test_get_notice_by_regid(self):
        with self.settings(
            RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
            RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            regid = "9136CCB8F66711D5BE060004AC494FFE"

            notices = _get_notices_by_regid(regid)
            #has category
            self.assertEquals(notices[0].myuw_category, "Holds")
            #no category
            self.assertEquals(notices[1].myuw_category, UNKNOWN_CATEGORY_NAME)

            #no regid
            notices = _get_notices_by_regid(None)
            self.assertEquals(notices, None)

            #bad regid
            notices = _get_notices_by_regid("1234")
            self.assertEquals(notices, None)