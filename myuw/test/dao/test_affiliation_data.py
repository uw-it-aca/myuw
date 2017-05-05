import os
from unittest2 import TestCase
from myuw.dao.affiliation_data import (_load_data_from_file,
                                       get_data_for_affiliations)
from myuw.exceptions import InvalidAffiliationDataFile
from myuw.models.res_category_link import ResCategoryLink


def _make_path(file_name):
    return os.path.join('test', file_name)


class TestLoadAffiliationData(TestCase):
    def test_load_bad_file_headers(self):
        with self.assertRaises(InvalidAffiliationDataFile):
            _load_data_from_file(_make_path('missing_headers'))

    def test_load_bad_file_pce(self):
        with self.assertRaises(InvalidAffiliationDataFile):
            _load_data_from_file(_make_path('bad_pce_status'))

    def test_load_valid_file(self):
        data = _load_data_from_file(_make_path('basic_valid'))
        self.assertEquals(len(data), 5)

        self.assertEquals(data[0]['campus'], 'seattle')
        self.assertEquals(data[1]['campus'], 'seattle')
        self.assertEquals(data[2]['campus'], 'bothell')
        self.assertEquals(data[3]['campus'], None)
        self.assertEquals(data[4]['campus'], None)

        self.assertEquals(data[0]['affiliation'], 'undergrad')
        self.assertEquals(data[1]['affiliation'], 'grad')
        self.assertEquals(data[2]['affiliation'], 'grad')
        self.assertEquals(data[3]['affiliation'], None)
        self.assertEquals(data[4]['affiliation'], None)

        self.assertFalse(data[0]['pce'])
        self.assertTrue(data[1]['pce'])
        self.assertTrue(data[2]['pce'] is None)
        self.assertTrue(data[3]['pce'] is None)
        self.assertTrue(data[4]['pce'] is None)

    def test_data_from_file(self):
        links = get_data_for_affiliations(file=_make_path('basic_valid'),
                                          affiliations={'seattle': True,
                                                        'undergrad': True,
                                                        'grad': False,
                                                        'pce': False,
                                                        })

        self.assertEquals(len(links), 3)
        self.assertEquals(links[0]['extra'], 'ok')
        self.assertEquals(links[1]['extra'], 'ok4')
        self.assertEquals(links[2]['extra'], 'ok5')

    def test_data_from_model(self):
        ResCategoryLink.objects.all().delete()
        links = get_data_for_affiliations(model=ResCategoryLink,
                                          affiliations={'seattle': True,
                                                        'undergrad': True,
                                                        'grad': False,
                                                        'pce': False,
                                                        })

        self.assertEquals(len(links), 0)

        ResCategoryLink.objects.create(title="link1",
                                       url="http://example.com?q=0")
        ResCategoryLink.objects.create(title="link2",
                                       url="http://example.com?q=1",
                                       affiliation='undergrad',
                                       campus='seattle',
                                       pce=True)
        ResCategoryLink.objects.create(title="link3",
                                       url="http://example.com?q=2",
                                       affiliation='undergrad',
                                       campus='seattle',
                                       pce=False)

        links = get_data_for_affiliations(model=ResCategoryLink,
                                          affiliations={'seattle': True,
                                                        'undergrad': True,
                                                        'grad': False,
                                                        'pce': False,
                                                        })
        self.assertEquals(len(links), 2)
        self.assertEqual(links[0].title, 'link1')
        self.assertEqual(links[0].url, 'http://example.com?q=0')
        self.assertEqual(links[1].title, 'link3')
        self.assertEqual(links[1].url, 'http://example.com?q=2')

    def test_unique_data(self):
        ResCategoryLink.objects.all().delete()
        ResCategoryLink.objects.create(title="link1",
                                       url="http://example.com?q=0")
        ResCategoryLink.objects.create(title="link2",
                                       url="http://example.com?q=0")
        ResCategoryLink.objects.create(title="link3",
                                       url="http://example.com?q=0")
        ResCategoryLink.objects.create(title="link4",
                                       url="http://example.com?q=0")

        links = get_data_for_affiliations(model=ResCategoryLink)
        self.assertEquals(len(links), 4)

        links = get_data_for_affiliations(model=ResCategoryLink,
                                          unique=lambda x: x.url)
        self.assertEquals(len(links), 1)
        self.assertEquals(links[0].title, "link1")
