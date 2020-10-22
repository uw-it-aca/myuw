from myuw.views.page import page
from myuw.util.page_view import page_view
from myuw.dao.term import get_specific_term


@page_view
def future_quarters(request, quarter):
    term_label = quarter.split(",")
    term = get_specific_term(term_label[0], term_label[1])
    term_data = {
        "year": term.year,
        "quarter": term.quarter,
        'summer_term': term_label[2] if len(term_label) == 3 else "",
        "first_day_quarter": term.first_day_quarter,
        "last_day_instruction": term.last_day_instruction,
        "aterm_last_date": term.aterm_last_date,
        "bterm_first_date": term.bterm_first_date,
    }
    context = {
        'future_term': quarter,
        'term_data': term_data
    }
    return page(request, 'future_quarters.html', context=context)
