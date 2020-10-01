from django.test import TestCase
from django.core.management import call_command


class TestFlushMemcache(TestCase):

    def test_run(self):
        return
        call_command('memcache', '-f')
        call_command('memcache', '--flush')
        call_command('memcache')
