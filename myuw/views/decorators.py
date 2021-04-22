# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.shortcuts import render
from myuw.authorization import can_override_user, is_myuw_admin
from blti import BLTI, BLTIException
from blti.validators import Roles

BLTI_USER_LOGIN = 'custom_canvas_user_login_id'


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


def blti_admin_required(func):
    def wrapper(request, *args, **kwargs):
        try:
            blti_session = BLTI().get_session(request)

            # Verify that the user is LTI Teacher or Admin
            blti_roles = BLTIRoles()
            blti_roles.validate(blti_session, visibility=blti_roles.ADMIN)

            # Set the user in US
            user = blti_session.get(BLTI_USER_LOGIN)
            request.session['_us_original_user'] = user
        except BLTIException:
            return render(request, 'no_access.html', {})

        return func(request, *args, **kwargs)
    return wrapper
