# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import skipIf

from django.test.utils import override_settings
from django.urls import reverse_lazy

from myuw.models import VisitedLinkNew
from myuw.test.api import MyuwApiTest, missing_url, require_url


@require_url('myuw_outbound_link')
@override_settings(LOGIN_URL=reverse_lazy('saml_login'))
class TestViewsLinkAdmin(MyuwApiTest):

    @skipIf(missing_url("myuw_outbound_link"),
            "myuw_outbound_link urls not configured")
    def test_outbound_link(self):
        link_url = "https%3A%2F%2Fhr.uw.edu%2F"
        label = ('.......................................................'
                 '.......................................................')
        url = f"/out/?u={link_url}&l={label}"
        self.set_user('javerage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        vlinks = VisitedLinkNew.objects.all()
        self.assertEqual(len(vlinks), 1)
        VisitedLinkNew.objects.all().delete()

        url = "/out?u={}&l={}".format(
            "https%3A%2F%2Fcoda.uw.edu%2F%232020-spring-TRAIN-100-A",
            "Course%20Dashboard%20for%20TRAIN%20100%20A")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        vlinks = VisitedLinkNew.objects.all()
        self.assertEqual(len(vlinks), 1)
        self.assertEqual(vlinks[0].label, "Course Dashboard for TRAIN 100 A")
        VisitedLinkNew.objects.all().delete()

        url = "/out?u={}&l=".format(
            "https%3A%2F%2Fcoda.uw.edu%2F%232020-spring-TRAIN-100-A")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        vlinks = VisitedLinkNew.objects.all()
        self.assertEqual(len(vlinks), 1)
        self.assertEqual(vlinks[0].label, "")
