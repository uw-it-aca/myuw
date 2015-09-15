from django.test import TestCase
from django.conf import settings
from myuw.context_processors import has_less_compiled,\
    has_google_analytics


class TestContextProcessors(TestCase):
    def test_less_none(self):
        with self.settings(COMPRESS_PRECOMPILERS=None):
            del settings.COMPRESS_PRECOMPILERS
            values = has_less_compiled(None)
            self.assertEquals(values["has_less_compiled"], False)

    def test_less_empty(self):
        with self.settings(COMPRESS_PRECOMPILERS=()):
            values = has_less_compiled(None)
            self.assertEquals(values["has_less_compiled"], False)

    def test_less_other_precompilers(self):
        with self.settings(COMPRESS_PRECOMPILERS=(
                ('text/coffeescript',
                 'coffee --compile --stdio'),
                ('text/foobar',
                 'path.to.MyPrecompilerFilter'),)):
            values = has_less_compiled(None)
            self.assertEquals(values["has_less_compiled"], False)

    def test_less_has_less_precompiler(self):
        with self.settings(COMPRESS_PRECOMPILERS=(
                ('text/coffeescript',
                 'coffee --compile --stdio'),
                ('text/foobar',
                 'path.to.MyPrecompilerFilter'),
                ('text/less', 'lessc {infile} {outfile}'),)):
            values = has_less_compiled(None)
            self.assertEquals(values["has_less_compiled"], True)

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
