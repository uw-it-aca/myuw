from myuw.views.page import page
from myuw.util.page_view import page_view


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
