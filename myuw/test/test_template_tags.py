import json
from unittest.mock import patch, mock_open

from django.core.cache import cache
from django.test import TestCase, override_settings

from myuw.templatetags.hashing_tag import hash_netid
from myuw.templatetags.myuw_large_number_display import large_number
from myuw.templatetags.webpack_manifest import find_manifest_path, \
    get_webpack_manifest, render_webpack_entry, WebpackManifestNotFound, \
    WebpackEntryNotFound, FileExtensionHasNoMapping, CACHE_TAG


class TestNetidHash(TestCase):
    def test_netids(self):
        self.assertEquals(hash_netid('javerage'),
                          'c13c917a1822a8acd58c48d2c8c6880a')
        self.assertEquals(hash_netid('eight'),
                          '24d27c169c2c881eb09a065116f2aa5c')
        self.assertEquals(hash_netid('none'),
                          '334c4a4c42fdb79d7ebc3e73b517e6f8')


class TestLargeNumberDisplay(TestCase):
    def test_numbers(self):
        self.assertEquals(999, large_number(999))
        self.assertEquals('1K', large_number(1000))
        self.assertEquals('1K', large_number(1900))
        self.assertEquals('27K', large_number(27900))
        self.assertEquals('4M', large_number(4000000))
        self.assertEquals('3B', large_number(3000000000))


class TestWebpackManifest(TestCase):
    def setUp(self):
        self.mock_manifest = {
            'entries': {
                'test1': [
                    '0-123.js',
                    '0-123.css',
                    'test1-123.js',
                    'test1-123.css'
                ],
                'test2': [
                    '0-123.js',
                    '0-123.css',
                    'test2-123.js',
                    'test2-123.css'
                ],
            },
            'bundles': {
                '0-123.js': '/myuw/0-123.js',
                '0-123.css': '/myuw/0-123.css',
                'test1-123.js': '/myuw/test1-123.js',
                'test1-123.css': '/myuw/test1-123.css',
                'test2-123.js': '/myuw/test2-123.js',
                'test2-123.css': '/myuw/test2-123.css',
            },
        }

    @override_settings(STATICFILES_DIRS=["/static/myuw/"])
    @patch('os.path.isfile', return_value=True)
    def test_find_manifest_path(self, _):
        self.assertEquals(find_manifest_path(), '/static/myuw/manifest.json')

    @override_settings(STATICFILES_DIRS=["/static/myuw/"])
    @patch('os.path.isfile', return_value=False)
    def test_find_manifest_path_error(self, _):
        with self.assertRaises(
            WebpackManifestNotFound,
            msg="Manifest file with name (manifest.json) not \
                found in ['/static/myuw/']"
        ):
            find_manifest_path()

    @override_settings(STATICFILES_DIRS=["/static/myuw/"])
    @patch(
        'myuw.templatetags.webpack_manifest.find_manifest_path',
        return_value=''
    )
    def test_get_webpack_manifest(self, _):
        mock_data = json.dumps(self.mock_manifest)
        with patch('builtins.open', mock_open(read_data=mock_data)):
            self.assertEquals(get_webpack_manifest(), self.mock_manifest)

    @override_settings(STATICFILES_DIRS=["/static/myuw/"])
    @patch(
        'myuw.templatetags.webpack_manifest.find_manifest_path',
        return_value=''
    )
    def test_get_webpack_manifest_error(self, _):
        with patch('builtins.open', mock_open()) as m:
            m.side_effect = FileNotFoundError('')
            with self.assertRaises(
                WebpackManifestNotFound,
                msg="Manifest file with name (manifest.json) not \
                    found in ['/static/myuw/']"
            ):
                get_webpack_manifest()

    @patch('myuw.templatetags.webpack_manifest.get_webpack_manifest')
    def test_render_webpack_entry_1(self, mock):
        mock.return_value = self.mock_manifest
        self.assertEquals(
            render_webpack_entry('test1'),
            """<script src="/static/myuw/0-123.js" ></script>
<link rel="stylesheet" type="text/css" href="/static/myuw/0-123.css" >
<script src="/static/myuw/test1-123.js" ></script>
<link rel="stylesheet" type="text/css" href="/static/myuw/test1-123.css" >
"""
        )

    @patch('myuw.templatetags.webpack_manifest.get_webpack_manifest')
    def test_render_webpack_entry_2(self, mock):
        mock.return_value = self.mock_manifest
        self.assertEquals(
            render_webpack_entry('test2'),
            """<script src="/static/myuw/0-123.js" ></script>
<link rel="stylesheet" type="text/css" href="/static/myuw/0-123.css" >
<script src="/static/myuw/test2-123.js" ></script>
<link rel="stylesheet" type="text/css" href="/static/myuw/test2-123.css" >
"""
        )

    @patch('myuw.templatetags.webpack_manifest.get_webpack_manifest')
    def test_render_webpack_entry_1_attr(self, mock):
        mock.return_value = self.mock_manifest
        self.assertEquals(
            render_webpack_entry('test1', js='defer', css='test'),
            """<script src="/static/myuw/0-123.js" defer></script>
<link rel="stylesheet" type="text/css" href="/static/myuw/0-123.css" test>
<script src="/static/myuw/test1-123.js" defer></script>
<link rel="stylesheet" type="text/css" href="/static/myuw/test1-123.css" test>
"""
        )

    @patch('myuw.templatetags.webpack_manifest.get_webpack_manifest')
    def test_render_webpack_entry_error(self, mock):
        mock.return_value = self.mock_manifest
        with self.assertRaises(
            WebpackEntryNotFound,
            msg="Webpack entry with name no_existent not found in manifest."
        ):
            render_webpack_entry('no_existent')

    @patch('myuw.templatetags.webpack_manifest.get_webpack_manifest')
    def test_render_webpack_entry_error_ext(self, mock):
        self.mock_manifest['entries']['test1'].append('bundle.crazy')
        self.mock_manifest['bundles']['bundle.crazy'] = '/myuw/bundle.crazy'
        mock.return_value = self.mock_manifest
        with self.assertRaises(
            FileExtensionHasNoMapping,
            msg="File extension has not mapping crazy, available mappings \
{('js',): 'script', ('css',): 'style'}"
        ):
            cache.delete(CACHE_TAG.format('test1'))
            render_webpack_entry('test1')
