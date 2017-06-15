from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def profile(request):
    return page(request, template='profile.html')
