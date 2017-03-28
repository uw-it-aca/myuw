from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def search_res(request):
    return page(request, {}, template='search_res.html')
