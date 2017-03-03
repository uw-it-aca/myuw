from unittest2 import skipIf
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from myuw.test.api import missing_url, require_url, MyuwApiTest


@require_url('myuw_home')
class TestTextbook(MyuwApiTest):

    @skipIf(missing_url("myuw_textbooks_page"),
            "myuw_textbooks_page urls not configured")
    def test_textbook_current(self):
        url = reverse("myuw_textbooks_page")
        self.set_user("javerage")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['term'])
        self.assertIsNone(response.context['textbook'])
        self.assertEqual(response.context['year'], 2013)
        self.assertEqual(response.context['quarter'], 'spring')

        response = self.client.get(url + "/2013,spring/PHYS121AC")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['term'], u'2013,spring')
        self.assertEqual(response.context['textbook'], u'PHYS121AC')

    @skipIf(missing_url("myuw_textbooks_page"),
            "myuw_pref_new_site urls not configured")
    def test_textbook_future(self):
        url = reverse("myuw_textbooks_page")
        self.set_user("javerage")
        response = self.client.get(url + "/2013,autumn")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['term'], u'2013,autumn')
        self.assertIsNone(response.context['textbook'])

        response = self.client.get(url + "/2013,summer,a-term")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['term'], u'2013,summer,a-term')
        self.assertIsNone(response.context['textbook'])

        response = self.client.get(url + "/2013,summer,b-term")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['term'], u'2013,summer,b-term')
        self.assertIsNone(response.context['textbook'])

        response = self.client.get(url + "/2013,summer,b-term/TRAIN101A")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['term'], u'2013,summer,b-term')
        self.assertEqual(response.context['textbook'], u'TRAIN101A')
