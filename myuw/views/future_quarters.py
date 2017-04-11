from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def future_quarters(request, quarter):
    context = {
        'future_term': quarter
    }
    return page(request, context=context, template='future_quarters.html')
