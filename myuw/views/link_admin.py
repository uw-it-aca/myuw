from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import logging
from myuw.views import admin_required, set_admin_wrapper_template
from myuw.models import VisitedLink


@login_required
@admin_required('MYUW_ADMIN_GROUP')
def popular_links(request):
    logger = logging.getLogger(__name__)

    kwargs = {}
    for check in dir(VisitedLink):
        if check.find('is_') == 0:
            if check in request.GET:
                kwargs[check] = True

    popular = VisitedLink.get_popular(**kwargs)
    context = {'popular': popular, 'checked': kwargs}
    set_admin_wrapper_template(context)
    return render(request, "admin/popular_links.html", context)
