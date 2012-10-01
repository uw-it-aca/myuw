from django.http import HttpRequest
from django.shortcuts import redirect
from django.conf import settings
import logging
from myuw_mobile.user import UserService
from myuw_mobile.dao.pws import Person as PersonDao
from myuw_mobile.logger.timer import Timer

logger = logging.getLogger('myuw_mobile.views.user_login')

def user_login(request):
    user_service = UserService(request)
    netid = user_service.get_user()

    if not netid:
        return #a static error page 

    if PersonDao(user_service).is_student():
        return redirect("myuw_mobile.views.page.index")

    if hasattr(settings, "MYUW_USER_SERVLET_URL"):
        return redirect(settings.MYUW_USER_SERVLET_URL)
    else:
        return redirect("https://myuw.washington.edu/servlet/user")
