from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from restclients.gws import GWS
import logging
from myuw_mobile.user import UserService
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.util import log_invalid_netid_response, log_success_response

def support(request):
    timer = Timer()
    logger = logging.getLogger('myuw_mobile.views.support')

    user_service = UserService()
    user_service.get_user()
    # Do the group auth here.

    if not hasattr(settings, "MYUW_ADMIN_GROUP"):
        print "You must have a group in GWS defined as your admin group."
        print 'Configure that using MYUW_ADMIN_GROUP="u_foo_bar"'
        raise Exception("Missing MYUW_ADMIN_GROUP in settings")


    actual_user = user_service.get_original_user()
    if not actual_user:
        log_invalid_netid_response(logger, timer)
        return

    gws = GWS()
    members = gws.get_effective_members(settings.MYUW_ADMIN_GROUP)

    is_admin = False

    for member in members:
        if member.uwnetid == actual_user:
            is_admin = True
            break

    if is_admin == False:
        return  HttpResponseRedirect("/mobile")

    if "override_as" in request.POST:
        user_service.set_override_user(request.POST["override_as"])

    if "clear_override" in request.POST:
        user_service.clear_override()

    context = {
        'original_user': user_service.get_original_user(),
        'override_user': user_service.get_override_user(),
    }
    log_success_response(logger, timer)
    return render_to_response('support.html',
                              context,
                              context_instance=RequestContext(request))


