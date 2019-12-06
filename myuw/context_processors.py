# Determins if the requesting device is a native hybrid app (android/ios)


def is_hybrid(request):

    return {
        'is_hybrid': 'HTTP_MYUW_HYBRID' in request.META
    }
