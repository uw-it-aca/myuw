from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import logging
from django.conf import settings
from restclients.gws import GWS
from myuw_mobile.dao.sws import Quarter as QuarterDao
from myuw_mobile.logger.timer import Timer
from myuw_mobile.user import UserService

logger = logging.getLogger('myuw_mobile.views.page')

#@mobile_template('{mobile/}index.html')
def index(request):
    timer = Timer()
    context = {'year': None,
               'quarter': None,
               'home_url': '/mobile',
               'err': None}

    if not request.is_secure():
        context['err'] = 'Not https, abort!'
    else:
        user_service = UserService(request)
        netid = user_service.get_user()

        if not netid:
            context['err'] = 'Invalid netid!'
        else:
            request.session["user_netid"] = netid

            cur_term = QuarterDao(user_service).get_cur_quarter()
            if not cur_term:
                context['err'] = 'No current quarter data!'
            else:
                context['year'] = cur_term.year
                context['quarter'] = cur_term.quarter

        logger.info("index time=%s", timer.get_elapsed,
                    user_service.get_log_user_info())

    return render_to_response('index.html',
                              context,
                              context_instance=RequestContext(request))

