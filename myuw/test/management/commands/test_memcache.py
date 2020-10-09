from django.test import TestCase
from django.test.utils import override_settings
from django.core.management import call_command


class TestFlushMemcache(TestCase):
    @override_settings(MEMCACHED_SERVERS=['localhost:11211'])
    def test_run(self):
        call_command('memcache', '-f')
        call_command('memcache', '--flush')
        call_command('memcache')
