import logging
from commonconf import settings


logger = logging.getLogger(__name__)


def has_less_compiled(request):
    """ See if django-compressor is being used to precompile less
    """
    key = getattr(settings, "COMPRESS_PRECOMPILERS", ())

    has_less_precompiler = False
    for entry in key:
        if entry[0] == "text/less":
            has_less_precompiler = True
    return {'has_less_compiled': has_less_precompiler}


def less_not_compiled(request):
    return {}


def has_google_analytics(request):
    ga_key = getattr(settings, 'GOOGLE_ANALYTICS_KEY', False)
    logger.info("has_google_analytics: %s", (ga_key is not False))
    return {
        'GOOGLE_ANALYTICS_KEY': ga_key,
        'has_google_analytics': ga_key
    }
