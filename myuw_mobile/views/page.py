from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
import logging
from userservice.user import UserService
from myuw_mobile.dao.term import get_current_quarter
from myuw_mobile.dao.affiliation import get_all_affiliations
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_invalid_netid_response, log_success_response_with_affiliation
from myuw_mobile.views.rest_dispatch import invalid_session
from myuw_mobile.dao.uwemail import get_email_forwarding_for_current_user

#@mobile_template('{mobile/}index.html')
def index(request,
          year=None, 
          quarter=None,
          summer_term=None):
    timer = Timer()
    logger = logging.getLogger('myuw_mobile.views.page.index')

    context = {"year": year,
               "quarter": quarter,
               "summer_term": summer_term,
               "home_url": "/mobile",
               "err": None,
               "user": {
                   "netid": None,
                   "affiliations": get_all_affiliations()
               }}

    netid = UserService().get_user()
    if not netid:
        log_invalid_netid_response(logger, timer)
        return invalid_session()

    my_uwemail_forwarding = get_email_forwarding_for_current_user()
    if my_uwemail_forwarding is not None and my_uwemail_forwarding.is_active():
        context["user"]["email_is_uwgmail"] = my_uwemail_forwarding.is_uwgmail()
        context["user"]["email_is_uwlive"] = my_uwemail_forwarding.is_uwlive()

    context["user"]["netid"] = netid
    if year is None or quarter is None:
        cur_term = get_current_quarter()
        if cur_term is None:
            context["err"] = "No current quarter data!"
            log_data_not_found_response(logger, timer)
        else:
            context["year"] = cur_term.year
            context["quarter"] = cur_term.quarter
    else:
        pass
    log_success_response_with_affiliation(logger, timer)
    return render_to_response("index.html",
                              context,
                              context_instance=RequestContext(request))




