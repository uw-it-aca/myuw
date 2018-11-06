from myuw.util.page_view import page_view
from myuw.views.page import page


@page_view
def index(request):
    return page(request, 'index.html', add_quicklink_context=True)
