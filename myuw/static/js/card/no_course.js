var CardWithNoCourse = {
    render: function( term ) {
        // If there's already a rendered no_course card,
        // don't draw a second one on the screen - MUWM-1924
        if ($(".no_courses_dupe_blocker").length) {
            return "";
        }
        var quarter = window.term.year + ' ' + window.term.quarter;
        var term_str = (term === 'current' ?
                        (window.card_display_dates.is_summer ?
                         (window.card_display_dates.is_after_summer_b_start ?
                          'Summer Term B'
                          : 'Summer Term A')
                         : quarter)
                        : term);
        var quarter_str = (term === 'current' ? quarter : titilizeTerm(term));
        if (!quarter_str.match(/[Tt]erm$/)) {
            quarter_str = quarter_str + ' quarter';
        }

        var source   = $("#card_with_no_course").html();
        var template = Handlebars.compile(source);
        var raw = template({term: term_str,
                            quarter: quarter_str});
        return raw;
    }
};
