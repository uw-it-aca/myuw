import logging
from django.core.management.base import BaseCommand, CommandError
from myuw.util.cache_implementation import MyUWMemcachedCache

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('action', type=str,
                            help="param1: flush|stats (default)")

    def handle(self, *args, **options):
        action = options['action']
        client = MyUWMemcachedCache().client
        logger.info("Stats {}".format(client.stats()))
        if action == "flush":
            logger.info("Flush all successful: {}".format(client.flush_all()))
            logger.info("Stats after flush: {}".format(client.stats()))
