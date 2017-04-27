from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def textbooks(request, term=None, textbook=None):
    context = {
        'term': term,
        'textbook': textbook
    }
    return page(request, context=context, template='textbooks.html')
