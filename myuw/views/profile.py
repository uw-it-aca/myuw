from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def profile(request):
    context = {
        "page_title": "Profile"
    }
    return page(request, context, template='profile.html')
