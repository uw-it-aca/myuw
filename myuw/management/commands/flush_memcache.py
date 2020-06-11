import logging
from rc_django.cache_implementation.memcache import MemcachedCache


logger = logging.getLogger(__name__)

class Command(BaseCommand):

    def handle(self, *args, **options):
        client = MyUWMemcachedCache().client
        logger.info("Stats before flush: {}".format(client.stats()))
        logger.info("Flush all successful: {}".format(client.flush_all()))
        logger.info("Stats after flush: {}".format(client.stats()))
