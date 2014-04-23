from django.conf import settings

def has_less_compiled(request):
    """ See if django-compressor is being used to precompile less
    """
    if settings.COMPRESS_ENABLED:
        return {'has_less_compiled': True}
    else:
        return {'has_less_compiled': False}


def less_not_compiled(request):
    return { }
