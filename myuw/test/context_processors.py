from django.test import TestCase
from django.conf import settings
from myuw.context_processors import has_google_analytics


class TestContextProcessors(TestCase):

    def test_has_google_analytics(self):
        with self.settings(GOOGLE_ANALYTICS_KEY="ga_1234"):
            values = has_google_analytics(None)
            self.assertTrue(values["has_google_analytics"])
            self.assertEquals(values["GOOGLE_ANALYTICS_KEY"], "ga_1234")

    def test_missing_google_analytics(self):
        with self.settings(GOOGLE_ANALYTICS_KEY=None):
            del settings.GOOGLE_ANALYTICS_KEY
            values = has_google_analytics(None)
            self.assertFalse(values["has_google_analytics"])
