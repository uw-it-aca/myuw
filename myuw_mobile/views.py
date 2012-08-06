from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from myuw_api.quarter import Quarter
from myuw_api.person import Person

def index(request):
    regid = Person().get_regid ('student1')
        
    cur_term = Quarter().get_cur_quarter()
        
    context = {'year': cur_term.year,
               'quarter_name': cur_term.quarter,
               'regid': regid,
               'myuw_base_url': ''}
    return render_to_response('mobile/index.html', 
                              context, 
                              context_instance=RequestContext(request))


