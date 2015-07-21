from django.test import TestCase
from myuw_mobile.dao.notice import _get_notices_by_regid


FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_PWS = 'restclients.dao_implementation.pws.File'


class TestNotices(TestCase):

    def test_get_notice_by_regid(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):

            # no regid
            notices = _get_notices_by_regid(None)
            self.assertEquals(notices, None)

            # bad regid
            notices = _get_notices_by_regid("1234")
            self.assertEquals(notices, None)

            regid = "9136CCB8F66711D5BE060004AC494FFE"
            notices = _get_notices_by_regid(regid)
            self.assertIsNotNone(notices)
            self.assertEquals(len(notices), 13)

            self.assertEquals(notices[0].custom_category, "Holds")
            self.assertEquals(notices[0].location_tags, ['notices_holds',
                                                         'reg_card_holds'])
            self.assertTrue(notices[0].is_critical)

            self.assertEquals(notices[12].custom_category,
                              "Fees & Finances")
            self.assertEquals(notices[12].location_tags,
                              ['tuition_aid_reminder_title'])
            self.assertFalse(notices[12].is_critical)
