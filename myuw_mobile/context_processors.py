from django.conf import settings

def less_not_compiled(request):
    """ See if django-compressor is being used to precompile less
    """
    if settings.COMPRESS_ENABLED:
        return {'less_not_compiled': False} 
    else:
        return {'less_not_compiled': True}

