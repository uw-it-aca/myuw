from unittest import skipIf
from django.urls import reverse
from django.test import Client
from django.test.utils import override_settings
from myuw.models import VisitedLinkNew
from myuw.views.link import outbound_link
from myuw.test.api import missing_url, require_url, MyuwApiTest
from django.urls import reverse_lazy


@require_url('myuw_outbound_link')
@override_settings(LOGIN_URL=reverse_lazy('saml_login'))
class TestViewsLinkAdmin(MyuwApiTest):

    @skipIf(missing_url("myuw_outbound_link"),
            "myuw_outbound_link urls not configured")
    def test_outbound_link(self):
        link_url = "https%3A%2F%2Fhr.uw.edu%2F"
        label = ('.......................................................'
                 '.......................................................')
        url = "/out/?u={}&l={}".format(link_url, label)
        self.set_user('javerage')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        vlinks = VisitedLinkNew.objects.all()
        self.assertEquals(len(vlinks), 1)
        VisitedLinkNew.objects.all().delete()

        url = "/out?u={}&l={}".format(
            "https%3A%2F%2Fcoda.uw.edu%2F%232020-spring-TRAIN-100-A",
            "Course%20Dashboard%20for%20TRAIN%20100%20A")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        vlinks = VisitedLinkNew.objects.all()
        self.assertEquals(len(vlinks), 1)
        self.assertEquals(vlinks[0].label, "Course Dashboard for TRAIN 100 A")
        VisitedLinkNew.objects.all().delete()

        url = "/out?u={}&l=".format(
            "https%3A%2F%2Fcoda.uw.edu%2F%232020-spring-TRAIN-100-A")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        vlinks = VisitedLinkNew.objects.all()
        self.assertEquals(len(vlinks), 1)
        self.assertEquals(vlinks[0].label, "")
