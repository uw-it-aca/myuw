import logging
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from myuw.util.cache import MyUWMemcachedCache

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-f", "--flush",
                            action="store_true", default=False,
                            help="Flush the cache")

    def handle(self, *args, **options):
        flush = options["flush"]
        client = MyUWMemcachedCache()
        # logger.info("Stats {}".format(client.stats()))
        if flush:
            try:
                logger.info("Flushed: {}".format(client.flush_all()))
            except Exception as ex:
                logger.error("Memcached: {}, Servers: {}".format(
                    ex, getattr(settings, "MEMCACHED_SERVERS")))
