from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def thrive_messages(request):
    return page(request, template='thrive_messages.html')
