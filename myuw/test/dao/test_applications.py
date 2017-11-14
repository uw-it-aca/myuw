from django.test import TestCase
from uw_sdbmyuw.util import fdao_sdbmyuw_override
from uw_sws.util import fdao_sws_override
from myuw.dao.applications import get_applications
from myuw.test import get_user_pass


@fdao_sws_override
@fdao_sdbmyuw_override
class TestApplications(TestCase):

    def test_applications(self):
        self.client.login(username="japplicant",
                          password=get_user_pass("japplicant"))
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
