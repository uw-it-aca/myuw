from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import logging
from myuw_api.sws_dao import Quarter
from myuw_api.pws_dao import Person

logger = logging.getLogger('myuw_mobile.views')

#@mobile_template('{mobile/}index.html')
def index(request):
    context = {'year': None,
               'quarter': None,
               'regid': None,
               'myuw_base_url': '',
               'err': None}
    person = Person()
    try:
        context['regid'] = person.get_regid ('javerage')
#        context['dirUrl'] = person.get_contact (context['regid'])
    except Exception:
        context['err'] = 'Failed to get regid'

    try:
        cur_term = Quarter().get_cur_quarter()
    except Exception as e:
        print e
        context['err'] = 'Failed to get quarter '
    else:
        context['year'] = cur_term['year']
        context['quarter'] = cur_term['quarter']
    print context

    return render_to_response('mobile/index.html', 
                              context,
                              context_instance=RequestContext(request))


