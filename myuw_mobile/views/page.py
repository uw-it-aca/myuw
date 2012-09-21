from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.conf import settings
from restclients.gws import GWS
import logging
from myuw_mobile.user import UserService
from myuw_mobile.dao.sws import Quarter as QuarterDao
from pws_util import is_valid_netid, is_student

logger = logging.getLogger('myuw_mobile.views.page')

gws = GWS()

#@mobile_template('{mobile/}index.html')
def index(request):
    context = {'year': None,
               'quarter': None,
               'home_url': '',
               'err': None}

    netid = get_netid_from_session(request)
    if is_valid_netid(netid):
        request.session["user_netid"] = netid
    else:
        context['err'] = 'Invalid netid'

    try:
        cur_term = QuarterDao().get_cur_quarter()
    except Exception, message:
        logger.error(netid + " get_cur_quarter --> " + message)
        context['err'] = 'Failed to get quarter '
    else:
        context['year'] = cur_term.year
        context['quarter'] = cur_term.quarter

    return render_to_response('index.html',
                              context,
                              context_instance=RequestContext(request))

def myuw_login(request):
    netid = get_netid_from_session(request)
    if is_student(netid):
        return redirect("myuw_mobile.views.page.index")

    if hasattr(settings, "MYUW_USER_SERVLET_URL"):
        return redirect(settings.MYUW_USER_SERVLET_URL)
    else:
        return redirect("https://myuw.washington.edu/servlet/user")


def support(request):
    user_service = UserService(request.session)
    user_service.get_user()
    # Do the group auth here.

    if not hasattr(settings, "MYUW_ADMIN_GROUP"):
        print "You must have a group in GWS defined as your admin group."
        print 'Configure that using MYUW_ADMIN_GROUP="u_foo_bar"'
        raise Exception("missing config")


    actual_user = user_service.get_original_user()
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

    return render_to_response('support.html',
                              context,
                              context_instance=RequestContext(request))

def get_netid_from_session(request): 
    return UserService(request.session).get_user()

