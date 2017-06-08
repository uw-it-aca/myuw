from myuw.views.page import page
from myuw.util.page_view import page_view
from myuw.dao.term import get_term_from_quarter_string


@page_view
def future_quarters(request, quarter):
    term = get_term_from_quarter_string(quarter)
    term_data = {
        "year": term.year,
        "quarter": term.quarter,
        "first_day_quarter": term.first_day_quarter,
        "last_day_instruction": term.last_day_instruction,
        "aterm_last_date": term.aterm_last_date,
        "bterm_first_date": term.bterm_first_date
    }
    context = {
        'future_term': quarter,
        'term_data': term_data
    }
    return page(request, context=context, template='future_quarters.html')
