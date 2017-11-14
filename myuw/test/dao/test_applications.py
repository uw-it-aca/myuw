from unittest import TestCase

from uw_sdbmyuw.util import fdao_sdbmyuw_override
from uw_sws.util import fdao_sws_override

from myuw.dao.applications import get_applications
from myuw.test.api import MyuwApiTest


@fdao_sws_override
@fdao_sdbmyuw_override
class TestApplications(MyuwApiTest):

    def test_applications(self):
        self.set_netid("japplicant")

        applications = get_applications()

        self.assertEqual(len(applications), 3)

        seattle_application = None
        bothell_application = None
        tacoma_application = None

        for application in applications:
            if application.is_seattle:
                seattle_application = application
            elif application.is_tacoma:
                tacoma_application = application
            elif application.is_bothell:
                bothell_application = application

        self.assertIsNotNone(seattle_application)
        self.assertIsNotNone(bothell_application)
        self.assertIsNotNone(tacoma_application)

