from myuw.models import MigrationPreference
from myuw.dao.user import display_onboard_message
from myuw.test import get_request_with_user
from myuw.test.api import MyuwApiTest


class TestBannerMessage(MyuwApiTest):

    def test_close_banner_msg(self):
        self.set_user('bill')
        resp = self.get_response_by_reverse('myuw_close_banner_message')
        self.assertEqual(resp.content, '{"done": true}')

        req = get_request_with_user('bill')
        self.assertFalse(display_onboard_message(req))
