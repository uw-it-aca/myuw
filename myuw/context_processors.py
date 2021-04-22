# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# Determins if the requesting device is a native hybrid app (android/ios)


def is_hybrid(request):

    return {
        'is_hybrid': 'MyUW_Hybrid/1.0' in request.META.get(
            'HTTP_USER_AGENT', 'NONE')
    }
