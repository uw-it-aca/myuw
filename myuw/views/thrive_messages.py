from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from myuw.util.performance import log_response_time
from myuw.views.page import page


@login_required
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@log_response_time
def thrive_messages(request):
    context = {
        'page_title': 'Thrive Messages'
    }
    return page(request, context=context, template='thrive_messages.html')
