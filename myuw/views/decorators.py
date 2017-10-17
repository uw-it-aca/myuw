from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myuw.dao.gws import is_in_admin_group
from userservice.user import set_override_user, clear_override
from blti import BLTI, BLTIException
from blti.validators import BLTIRoles


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
            blti_roles = BLTIRoles()
            blti_roles.validate(blti_session, visibility=blti_roles.ADMIN)
            login_id = blti_session.get('custom_canvas_user_login_id')
            set_override_user(request, login_id)  # TODO: don't use override
        except BLTIException:
            return render(request, 'no_access.html', {})

        return func(request, *args, **kwargs)
    return wrapper
