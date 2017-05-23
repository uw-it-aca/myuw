from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def notices(request):
    context = {
        "page_title": "Notices"
    }
    return page(request, context, template='notices.html')
