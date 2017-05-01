from myuw.views.page import page, try_prefetch
from myuw.util.page_view import page_view
from myuw.dao.quicklinks import get_quicklink_data
from myuw.dao.affiliation import get_all_affiliations


@page_view
def teaching(request,
             year=None,
             quarter=None,
             summer_term=None):
    context = {
        "year": year,
        "quarter": quarter,
        "summer_term": summer_term
    }

    failure = try_prefetch(request)
    if failure:
        return failure

    _add_quicklink_context(request, context)
    return page(request, context, template='teaching.html')


@page_view
def teaching_section(request,
                     section,
                     year=None,
                     quarter=None,
                     summer_term=None):
    context = {
        "section": section,
        "year": year,
        "quarter": quarter,
        "summer_term": summer_term
    }
    return page(request, context, template='teaching_section.html')


@page_view
def student_photo_list(request,
                       section,
                       year=None,
                       quarter=None,
                       summer_term=None):
    context = {
        "section": section,
        "year": year,
        "quarter": quarter,
        "summer_term": summer_term
    }
    return page(request, context, template='teaching/photo_list.html')


def _add_quicklink_context(request, context):
    link_data = get_quicklink_data()

    for key in link_data:
        context[key] = link_data[key]
