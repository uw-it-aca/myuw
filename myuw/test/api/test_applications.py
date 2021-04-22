# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from django.test import TestCase
from uw_pws.util import fdao_pws_override
from uw_sdbmyuw.util import fdao_sdbmyuw_override
from uw_sws.util import fdao_sws_override
from myuw.dao.applications import get_applications
from myuw.test import get_user_pass, get_user
from myuw.test.api import MyuwApiTest, require_url


@fdao_sws_override
@fdao_pws_override
@fdao_sdbmyuw_override
@require_url("myuw_applications_api")
class TestApplications(MyuwApiTest):

    def get_applications_response(self, netid, adate=None):
        self.set_user(netid)
        if adate is not None:
            self.set_date(adate)
        return self.get_response_by_reverse('myuw_applications_api')

    def test_applications(self):
        response = self.get_applications_response("javerage")
        self.assertEqual(response.status_code, 404)

        response = self.get_applications_response("japplicant")
        applications = json.loads(response.content)

        self.assertEqual(len(applications), 3)

        seattle_application = None
        bothell_application = None
        tacoma_application = None

        for application in applications:
            if application['is_seattle']:
                seattle_application = application
            elif application['is_tacoma']:
                tacoma_application = application
            elif application['is_bothell']:
                bothell_application = application

        self.assertIsNotNone(seattle_application)
        self.assertIsNotNone(bothell_application)
        self.assertIsNotNone(tacoma_application)

    def test_user_wo_system_key(self):
        response = self.get_applications_response("none")
        self.assertEqual(response.content, b"[]")
