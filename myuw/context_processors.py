def is_hybrid(request):
    
    try:
       hybridapp = request.META['HTTP_MYUW_HYBRID']
    except:
        hybridapp = False

    return {
        'is_hybrid': hybridapp
    }
