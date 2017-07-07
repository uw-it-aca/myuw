from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def teaching(request,
             year=None,
             quarter=None):
    context = get_context(year, quarter)
    return page(request, context, template='teaching.html')


@page_view
def teaching_section(request,
                     year,
                     quarter,
                     section):
    context = get_context(year, quarter, section)
    return page(request, context, template='teaching_section.html')


@page_view
def student_photo_list(request,
                       year,
                       quarter,
                       section):
    context = get_context(year, quarter, section)
    return page(request, context, template='teaching/photo_list.html')


def get_context(year, quarter, section=None):
    context = {}
    if year and quarter:
        context = {
            "display_term": {"year": year,
                             "quarter": quarter},
            }
    if section:
        context["section"] = "%s,%s,%s" % (year, quarter, section)
    return context
