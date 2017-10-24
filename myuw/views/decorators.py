from django.shortcuts import render
from myuw.dao.gws import is_in_admin_group
from blti import BLTI, BLTIException
from blti.validators import BLTIRoles

BLTI_USER_LOGIN = 'custom_canvas_user_login_id'


def admin_required(group_key):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not is_in_admin_group(group_key):
                return render(request, 'no_access.html', {})

            return func(request, *args, **kwargs)
        return wrapper
    return decorator


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
