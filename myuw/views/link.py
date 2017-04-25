from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from myuw.dao.affiliation import get_all_affiliations
from myuw.views import prefetch_resources
from myuw.models import VisitedLink
import re


def outbound_link(request):
    url = request.POST['url']

    if not re.match('^https?://', url):
        return HttpResponse(status=404)

    prefetch_resources(request)
    affiliations = get_all_affiliations(request)

    is_student_employee = affiliations['stud_employee']
    VisitedLink.objects.create(username=request.user.username,
                               url=url,
                               is_student=affiliations['student'],
                               is_undegrad=affiliations['undergrad'],
                               is_grad_student=affiliations['grad'],
                               is_employee=affiliations['employee'],
                               is_faculty=affiliations['faculty'],
                               is_seattle=affiliations['seattle'],
                               is_tacoma=affiliations['tacoma'],
                               is_bothell=affiliations['bothell'],
                               is_pce=affiliations['pce'],
                               is_student_employee=is_student_employee,
                               )

    return HttpResponseRedirect(url)
