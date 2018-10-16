from django.urls import reverse
from userservice.user import UserService
from myuw.models import MigrationPreference, User
from myuw.test import get_request_with_user
from myuw.test.api import MyuwApiTest, VALIDATE, OVERRIDE


class TestBannerMessage(MyuwApiTest):

    def test_close_banner_msg(self):
        self.set_user('bill')
        resp = self.get_response_by_reverse('myuw_close_banner_message')
        self.assertEqual(resp.content, b'{"done": true}')

        # remove the entry in DB (delete CASCADE)
        obj = User.objects.get(uwnetid='bill')
        obj.delete()

        resp = self.get_response_by_reverse('myuw_close_banner_message')
        self.assertEqual(resp.content, b'{"done": true}')

        user = User.objects.get(uwnetid='bill')
        self.assertIsNotNone(str(user))
        pref = MigrationPreference.objects.get(user=user)
        self.assertIsNotNone(str(pref))

    def test_close_banner_msg_error_case(self):
        self.set_user('0000')
        resp = self.get_response_by_reverse('myuw_close_banner_message')
        self.assertEqual(resp.content, b'No valid userid in session')

    def test_turn_off_pop_up(self):
        self.set_user('bill')
        resp = self.get_response_by_reverse('myuw_turn_off_tour_popup')
        self.assertEqual(resp.content, b'{"done": true}')

    def test_turn_off_pop_up_error_case(self):
        self.set_user('0000')
        resp = self.get_response_by_reverse('myuw_turn_off_tour_popup')
        self.assertEqual(resp.content, b'No valid userid in session')

    def test_close_banner_msg_when_override(self):
        with self.settings(DEBUG=False,
                           MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE=True):
            self.set_user('javerage')
            self.set_userservice_override("bill")
            self.assertEquals(UserService().get_override_user(), "bill")
            resp = self.get_response_by_reverse('myuw_close_banner_message')
            self.assertEqual(resp.status_code, 401)

    def test_turn_off_pop_up_when_override(self):
        with self.settings(DEBUG=False,
                           MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE=True):
            self.set_user('javerage')
            self.set_userservice_override("bill")
            self.assertEquals(UserService().get_override_user(), "bill")
            resp = self.get_response_by_reverse('myuw_turn_off_tour_popup')
            self.assertEqual(resp.status_code, 401)
