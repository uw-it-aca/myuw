from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def husky_experience(request):
    return page(request, 'husky_experience.html')
