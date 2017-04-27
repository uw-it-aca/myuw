from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def category(request, category=None, topic=None):
    context = {
        'category': category,
        'topic': topic
    }
    return page(request, context=context, template='category.html')
