from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.conf import settings
import logging
from userservice.user import UserService
from myuw.dao.term import get_current_quarter
from myuw.dao.affiliation import get_all_affiliations
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_data_not_found_response
from myuw.logger.logresp import log_invalid_netid_response
from myuw.logger.logresp import log_success_response_with_affiliation
from myuw.views.rest_dispatch import invalid_session
from myuw.dao.uwemail import get_email_forwarding_for_current_user
from myuw.dao.card_display_dates import get_card_visibilty_date_values
from myuw.logger.session_log import log_session


@login_required
def index(request,
          year=None,
          quarter=None,
          summer_term=None):
    timer = Timer()
    logger = logging.getLogger('myuw.views.page.index')

    context = {
        "year": year,
        "quarter": quarter,
        "summer_term": summer_term,
        "home_url": "/",
        "err": None,
        "user": {
            "netid": None,
            "affiliations": get_all_affiliations(request)
        },
        "card_display_dates": get_card_visibilty_date_values(request),
    }

    netid = UserService().get_user()
    if not netid:
        log_invalid_netid_response(logger, timer)
        return invalid_session()
    context["user"]["session_key"] = request.session.session_key
    log_session(netid, request.session.session_key, request)
    my_uwemail_forwarding = get_email_forwarding_for_current_user()
    if my_uwemail_forwarding is not None and my_uwemail_forwarding.is_active():
        c_user = context["user"]
        c_user["email_is_uwgmail"] = my_uwemail_forwarding.is_uwgmail()
        c_user["email_is_uwlive"] = my_uwemail_forwarding.is_uwlive()

    context["user"]["netid"] = netid
    if year is None or quarter is None:
        cur_term = get_current_quarter(request)
        if cur_term is None:
            context["err"] = "No current quarter data!"
            log_data_not_found_response(logger, timer)
        else:
            context["year"] = cur_term.year
            context["quarter"] = cur_term.quarter
    else:
        pass
    log_success_response_with_affiliation(logger, timer, request)
    return render_to_response("index.html",
                              context,
                              context_instance=RequestContext(request))
