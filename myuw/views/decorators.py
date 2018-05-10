from django.shortcuts import render
from myuw.dao.admin import is_admin, can_override
from blti import BLTI, BLTIException
from blti.validators import BLTIRoles

BLTI_USER_LOGIN = 'custom_canvas_user_login_id'


def admin_required(func):
    def wrapper(request, *args, **kwargs):
        if not is_admin():
            return render(request, 'no_access.html', {})

        return func(request, *args, **kwargs)
    return wrapper


def override_required(func):
    def wrapper(request, *args, **kwargs):
        if not can_override():
            return render(request, 'no_access.html', {})

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
