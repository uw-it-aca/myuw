import os
from django.test import TestCase
from django.core.management import call_command


class TestFlushMemcache(TestCase):

    def test_run(self):
        call_command('memcache', '-f')
        call_command('memcache', '--flush')
        call_command('memcache')
