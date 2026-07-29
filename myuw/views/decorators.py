# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.shortcuts import render

from myuw.authorization import can_override_user, is_myuw_admin


def admin_required(func):
    def wrapper(request, *args, **kwargs):
        if not is_myuw_admin(request):
            return render(request, 'no_access.html', status=403)

        return func(request, *args, **kwargs)
    return wrapper


def override_required(func):
    def wrapper(request, *args, **kwargs):
        if not can_override_user(request):
            return render(request, 'no_access.html', status=403)

        return func(request, *args, **kwargs)
    return wrapper
