from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def notices(request):
    return page(request, {}, template='notices.html')
