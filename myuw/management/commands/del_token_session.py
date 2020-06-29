from django.core.management.base import BaseCommand, CommandError
from myuw.util.sessions import delete_sessions, SCOPE_IDTOKEN


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('netid', type=str, help="param1: uwnetid")

    def handle(self, *args, **options):
        netid = options['netid']
        delete_sessions(netid, SCOPE_IDTOKEN)
