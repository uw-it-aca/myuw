from django.core.management.base import BaseCommand, CommandError
from myuw.util.sessions import delete_sessions, SCOPE_IDTOKEN


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('netid', type=str, help="param1: uwnetid")
        parser.add_argument('scope', type=str, help="param2: idtoken|all",
                            default=SCOPE_IDTOKEN)

    def handle(self, *args, **options):
        netid = options['netid']
        scope = options['scope']
        delete_sessions(netid, scope)
