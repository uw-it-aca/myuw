# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from unittest import TestCase
from myuw.dao.affiliation_data import (_load_data_from_file,
                                       get_data_for_affiliations)
from myuw.dao.exceptions import InvalidAffiliationDataFile
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
        self.assertEqual(len(data), 7)

        self.assertEqual(data[0]['campus'], 'seattle')
        self.assertEqual(data[1]['campus'], 'seattle')
        self.assertEqual(data[2]['campus'], 'bothell')
        self.assertEqual(data[3]['campus'], None)
        self.assertEqual(data[4]['campus'], None)

        self.assertEqual(data[0]['affiliation'], 'undergrad')
        self.assertEqual(data[1]['affiliation'], 'grad')
        self.assertEqual(data[2]['affiliation'], 'grad')
        self.assertEqual(data[3]['affiliation'], None)
        self.assertEqual(data[4]['affiliation'], None)

        self.assertFalse(data[0]['pce'])
        self.assertTrue(data[1]['pce'])
        self.assertTrue(data[2]['pce'] is None)
        self.assertTrue(data[3]['pce'] is None)
        self.assertTrue(data[4]['pce'] is None)

    def test_data_from_file(self):
        links = get_data_for_affiliations(file=_make_path('basic_valid'),
                                          affiliations={'seattle': True,
                                                        'tacoma': False,
                                                        'undergrad': True,
                                                        'grad': False,
                                                        'pce': False,
                                                        })

        self.assertEqual(len(links), 3)
        self.assertEqual(links[0]['extra'], 'ok')
        self.assertEqual(links[1]['extra'], 'ok4')
        self.assertEqual(links[2]['extra'], 'ok5')

    def test_data_from_model(self):
        ResCategoryLink.objects.all().delete()
        links = get_data_for_affiliations(model=ResCategoryLink,
                                          affiliations={'seattle': True,
                                                        'undergrad': True,
                                                        'grad': False,
                                                        'pce': False,
                                                        })

        self.assertEqual(len(links), 0)

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
        self.assertEqual(len(links), 2)
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
        self.assertEqual(len(links), 4)

        links = get_data_for_affiliations(model=ResCategoryLink,
                                          unique=lambda x: x.url)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].title, "link1")
