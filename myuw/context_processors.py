import logging
from commonconf import settings


logger = logging.getLogger(__name__)


def has_google_analytics(request):
    ga_key = getattr(settings, 'GOOGLE_ANALYTICS_KEY', False)
    logger.info("has_google_analytics: %s", (ga_key is not False))
    return {
        'GOOGLE_ANALYTICS_KEY': ga_key,
        'has_google_analytics': ga_key
    }
