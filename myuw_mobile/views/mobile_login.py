from django.http import HttpRequest
from django.shortcuts import redirect
from django.conf import settings
import logging
from myuw_mobile.user import UserService
from myuw_mobile.dao.pws import Person as PersonDao
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.util import log_invalid_netid_response, log_resp_time

def user_login(request):
    timer = Timer()
    logger = logging.getLogger('myuw_mobile.views.mobile_login.user_login')

    netid = UserService().get_user()
    if not netid:
        log_invalid_netid_response(logger, timer)
        return #a static error page 

    if PersonDao().is_student():
        log_resp_time(logger, 'to mobile', timer)
        return redirect("myuw_mobile.views.page.index")

    log_resp_time(logger, 'to desktop', timer)

    if hasattr(settings, "MYUW_USER_SERVLET_URL"):
        return redirect(settings.MYUW_USER_SERVLET_URL)
    else:
        return redirect("https://myuw.washington.edu/servlet/user")
