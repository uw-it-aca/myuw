from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def profile(request):
    context = {}
    return page(request, context, template='profile.html')
