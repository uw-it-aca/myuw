from myuw.models import MigrationPreference, User
from myuw.dao.user_pref import display_onboard_message
from myuw.test import get_request_with_user
from myuw.test.api import MyuwApiTest


class TestBannerMessage(MyuwApiTest):

    def test_close_banner_msg(self):
        self.set_user('bill')
        resp = self.get_response_by_reverse('myuw_close_banner_message')
        self.assertEqual(resp.content, '{"done": true}')

        obj = User.objects.get(uwnetid='bill')
        obj.delete()
        resp = self.get_response_by_reverse('myuw_close_banner_message')
        self.assertEqual(resp.content, '{"done": true}')

        req = get_request_with_user('bill')
        self.assertFalse(display_onboard_message(req))

    def test_error_case(self):
        self.set_user('0000')
        resp = self.get_response_by_reverse('myuw_close_banner_message')
        self.assertEqual(resp.content, 'No valid userid in session')
