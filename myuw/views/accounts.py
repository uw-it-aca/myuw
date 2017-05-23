from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def accounts(request):
    context = {
        "page_title": "Accounts"
    }
    return page(request, context, template='accounts.html')
