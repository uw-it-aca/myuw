from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import Http404

def index(request):
    if settings.DEBUG:
        return render_to_response("test/test.html",
                                  context_instance=RequestContext(request))
    else:
        raise Http404
