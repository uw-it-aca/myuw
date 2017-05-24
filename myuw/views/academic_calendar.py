from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def academic_calendar(request):
    return page(request, {}, template='academic_calendar.html')
