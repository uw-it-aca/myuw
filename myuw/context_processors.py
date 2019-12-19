# Determins if the requesting device is a native hybrid app (android/ios)


def is_hybrid(request):

    return {
        'is_hybrid': 'MyUW_Hybrid/1.0' in request.META['HTTP_USER_AGENT']
    }
