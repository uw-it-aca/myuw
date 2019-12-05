def is_hybrid(request):
    """ Checks request header for MyUW-Hybrid and returns true or false.
    """
    is_hybrid = False
    try request.META['HTTP_MYUW_HYBRID']:
        is_hybrid = True
    except:
        return is_hybrid
