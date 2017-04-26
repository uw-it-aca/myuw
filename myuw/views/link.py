from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from myuw.dao.affiliation import get_all_affiliations
from myuw.views import prefetch_resources
from myuw.models import VisitedLink
from urllib import unquote
import re


def outbound_link(request):
    url = unquote(request.GET.get('u', ''))

    if not re.match('^https?://', url):
        return HttpResponseRedirect("/")

    label = request.GET.get('l', None)
    if label:
        label = unquote(label)
    prefetch_resources(request)

    is_anon = True
    affiliations = {}

    if request.user.is_active:
        is_anon = False
        affiliations = get_all_affiliations(request)

    is_student_employee = affiliations.get('stud_employee', False)
    is_undergrad = affiliations.get('undergrad', False)
    VisitedLink.objects.create(username=request.user.username,
                               url=url,
                               label=label,
                               is_anonymous=is_anon,
                               is_student=affiliations.get('student', False),
                               is_undegrad=is_undergrad,
                               is_grad_student=affiliations.get('grad', False),
                               is_employee=affiliations.get('employee', False),
                               is_faculty=affiliations.get('faculty', False),
                               is_seattle=affiliations.get('seattle', False),
                               is_tacoma=affiliations.get('tacoma', False),
                               is_bothell=affiliations.get('bothell', False),
                               is_pce=affiliations.get('pce', False),
                               is_student_employee=is_student_employee,
                               )

    return HttpResponseRedirect(url)
