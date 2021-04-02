# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.models import UserCourseDisplay
from myuw.test.api import MyuwApiTest, fdao_sws_override, fdao_pws_override
from myuw.views.api.instructor_section_display import \
    CloseMinicard, PinMinicard
from myuw.test import get_request_with_user


@fdao_sws_override
@fdao_pws_override
class TestInstSectDetails(MyuwApiTest):

    def get_schedule(self, **kwargs):
        return self.get_response_by_reverse(
            'myuw_instructor_schedule_api',
            kwargs=kwargs,)

    def test_mini_card(self):
        self.set_user('bill')
        self.get_schedule(year=2013, quarter='spring')
        records = UserCourseDisplay.objects.all()
        self.assertEquals(len(records), 6)

        section_id = '2013,spring,PHYS,121/AC'
        resp = self.get_response_by_reverse(
            "myuw_inst_section_display_pin_mini",
            kwargs={'section_label': section_id})
        self.assertEqual(resp.content, b'{"done": true}')

        resp = self.get_response_by_reverse(
            "myuw_inst_section_display_close_mini",
            kwargs={'section_label': section_id})
        self.assertEqual(resp.content, b'{"done": true}')

        # test InvalidSectionID
        section_id = '2013,spring,PHYS,121/'
        resp = self.get_response_by_reverse(
            "myuw_inst_section_display_pin_mini",
            kwargs={'section_label': section_id})
        self.assertEqual(resp.status_code, 400)

        resp = self.get_response_by_reverse(
            "myuw_inst_section_display_close_mini",
            kwargs={'section_label': section_id})
        self.assertEqual(resp.status_code, 400)

        # test with a section DoesNotExist in DB
        section_id = '2013,spring,PHYS,121/AB'
        resp = self.get_response_by_reverse(
            "myuw_inst_section_display_pin_mini",
            kwargs={'section_label': section_id})
        self.assertEqual(resp.status_code, 543)

    def test_close_mini_card_when_override(self):
        with self.settings(DEBUG=False,
                           MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE=True):
            self.set_user('javerage')
            self.set_userservice_override("bill")
            section_id = '2013,spring,PHYS,121/AC'
            resp = self.get_response_by_reverse(
                "myuw_inst_section_display_close_mini",
                kwargs={'section_label': section_id})
            self.assertEqual(resp.status_code, 403)

    def test_pin_mini_card_when_override(self):
        with self.settings(DEBUG=False,
                           MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE=True):
            self.set_user('javerage')
            self.set_userservice_override("bill")
            section_id = '2013,spring,PHYS,121/AC'
            resp = self.get_response_by_reverse(
                "myuw_inst_section_display_pin_mini",
                kwargs={'section_label': section_id})
            self.assertEqual(resp.status_code, 403)
