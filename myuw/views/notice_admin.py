from myuw.views.decorators import admin_required
from myuw.views import set_admin_wrapper_template
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import logging


logger = logging.getLogger(__name__)


@login_required
@admin_required('MYUW_ADMIN_GROUP')
def manage_notices(request):
    context = {}
    set_admin_wrapper_template(context)
    return render(request, "admin/notices.html", context)
