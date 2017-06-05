from myuw.util.page_view import page_view
from myuw.views.page import page
from myuw.views.teaching import _add_quicklink_context


@page_view
def index(request, year=None, quarter=None, summer_term=None):
    context = {
        "year": year,
        "quarter": quarter,
        "summer_term": summer_term
    }
    _add_quicklink_context(request, context)
    return page(request, context, template='index.html')
