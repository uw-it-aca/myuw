from django.http import HttpRequest
from django.shortcuts import redirect
from django.conf import settings
import logging
from myuw_mobile.user import UserService
from myuw_mobile.dao.pws import Person as PersonDao
from myuw_mobile.logger.timer import Timer

def user_login(request):
    timer = Timer()
    logger = logging.getLogger('myuw_mobile.views.user_login')

    user_service = UserService()
    netid = user_service.get_user()

    if not netid:
        logger.info("user_login invalid netid, abort! time=%s",
                    timer.get_elapsed(),
                    user_service.get_log_user_info())
        return #a static error page 

    if PersonDao(user_service).is_student():
        logger.info("user_login to mobile page. time=%s",
                    timer.get_elapsed(),
                    user_service.get_log_user_info())
        return redirect("myuw_mobile.views.page.index")

    logger.info("user_login to desktop page. time=%s",
                timer.get_elapsed(),
                user_service.get_log_user_info())

    if hasattr(settings, "MYUW_USER_SERVLET_URL"):
        return redirect(settings.MYUW_USER_SERVLET_URL)
    else:
        return redirect("https://myuw.washington.edu/servlet/user")
