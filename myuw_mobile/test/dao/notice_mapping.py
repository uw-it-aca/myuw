from django.test import TestCase
from restclients.sws.notice import get_notices_by_regid
from myuw_mobile.dao.notice_mapping import map_notice_category


FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_PWS = 'restclients.dao_implementation.pws.File'


class TestMapNotices(TestCase):

    def test_get_notice_by_regid(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS):

            regid = "9136CCB8F66711D5BE060004AC494FFE"

            notices = get_notices_by_regid(regid)
            self.assertEquals(len(notices), 16)

            notice = map_notice_category(notices[0])
            self.assertEquals(notice.custom_category, "Holds")
            self.assertEquals(notice.location_tags, ['notices_holds',
                                                     'reg_card_holds'])
            self.assertTrue(notice.is_critical)

            notice = map_notice_category(notices[4])

            self.assertEquals(notice.custom_category, "Holds")
            self.assertEquals(notice.location_tags, ['notices_holds',
                                                     'reg_card_holds'])
            self.assertTrue(notice.is_critical)

            notice = map_notice_category(notices[9])
            self.assertEquals(notice.custom_category, "not a notice")
            self.assertEquals(notice.location_tags, [])
            self.assertFalse(notice.is_critical)
