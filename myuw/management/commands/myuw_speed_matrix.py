from django.core.management.base import BaseCommand, CommandError
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from myuw.urls import urlpatterns
from myuw.test.api import get_user, get_user_pass
from django.test.utils import override_settings
import time


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--url_name', help="The named MyUW URL to test")

    def handle(self, *args, **options):
        get_user('javerage')

        skipped = []

        print "URL Name,0 seconds,0.1 seconds,0.5 seconds,1.0 seconds"
        for pattern in urlpatterns:
            values = [pattern.name]

            if options["url_name"] and pattern.name != options["url_name"]:
                continue
            if pattern.name is None:
                skipped.append(pattern.regex.pattern)
                continue

            if pattern.name == 'myuw_book_api':
                skipped.append(pattern.regex.pattern)
                continue

            if pattern.name == 'myuw_links_api':
                skipped.append(pattern.regex.pattern)
                continue

            if pattern.name == 'myuw_myplan_api':
                skipped.append(pattern.regex.pattern)
                continue

            if pattern.name == 'myuw_future_summer_schedule_api':
                skipped.append(pattern.regex.pattern)
                continue

            if pattern.name == 'myuw_future_schedule_api':
                skipped.append(pattern.regex.pattern)
                continue

            delay = 0.0
            delay_values = [0.0, 0.1, 0.5, 1.0]
            for delay in delay_values:
                @override_settings(RESTCLIENTS_MOCKDATA_DELAY=delay)
                def run_it():

                    client = Client()
                    client.login(username='javerage',
                                 password=get_user_pass('javerage'))
                    t0 = time.time()
                    resp = client.get(reverse(pattern.name))
                    t1 = time.time()

                    return "%s" % (t1-t0)

                values.append(run_it())

            print ",".join(values)

        print "skipped: ", skipped
