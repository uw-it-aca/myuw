from django.http import HttpRequest
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
import logging
from userservice.user import UserService
from myuw.dao.pws import is_student
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_invalid_netid_response
from myuw.logger.logresp import log_response_time
from myuw.views.rest_dispatch import invalid_session


@login_required
def user_login(request):
    timer = Timer()
    logger = logging.getLogger('myuw.views.mobile_login.user_login')

    netid = UserService().get_user()
    if netid is None:
        log_invalid_netid_response(logger, timer)
        return invalid_session()

    if is_student():
        log_response_time(logger, 'to mobile', timer)
        return redirect("myuw.views.page.index")

    log_response_time(logger, 'to desktop', timer)

    if hasattr(settings, "MYUW_USER_SERVLET_URL"):
        return redirect(settings.MYUW_USER_SERVLET_URL)
    else:
        return redirect("https://myuw.washington.edu/servlet/user")
