from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def resources(request):
    return page(request, {}, template='resources.html')
