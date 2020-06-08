import logging
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sessions.models import Session
from myuw.logger.timer import Timer

logger = logging.getLogger('session')
log_format = "Deleted session of {}: {}"


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('netid', type=str,
                            help="param1: uwnetid")

    def handle(self, *args, **options):
        netid = options['netid']

        for session in Session.objects.all():
            data = session.get_decoded()
            if (data.get('uw_oidc_idtoken') and
                    data.get('_uw_original_user') == netid):
                logger.info(log_format.format(netid, data))
                session.delete()
