from django.test import TestCase
from myuw_mobile.dao.notice import UNKNOWN_CATEGORY_NAME, _get_notices_by_regid

class TestNotce(TestCase):

    def test_get_notice_by_regid(self):
        with self.settings(
            RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
            RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            regid = "9136CCB8F66711D5BE060004AC494FFE"

            notices = _get_notices_by_regid(regid)
            #has category
            self.assertEquals(notices[0].custom_category, "Holds")

            #location tags
            self.assertEquals(notices[0].location_tags, ['notices_holds', 'reg_card_holds'])

            #criticality
            self.assertEquals(notices[0].is_critical, True)

            #no regid
            notices = _get_notices_by_regid(None)
            self.assertEquals(notices, None)

            #bad regid
            notices = _get_notices_by_regid("1234")
            self.assertEquals(notices, None)