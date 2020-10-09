from myuw.util.page_view import page_view
from myuw.views.page import page


@page_view
def home(request):
    return page(request, 'home.html', add_quicklink_context=True)
