var CardWithNoCourse = {
    render: function( term ) {
        // If there's already a rendered no_course card,
        // don't draw a second one on the screen - MUWM-1924
        if ($(".no_courses_dupe_blocker").length) {
            return "";
        }
        var cur_qr = window.term.quarter;
        var term_str = (term === 'current' ?
                        (window.card_display_dates.is_summer ?
                         (window.card_display_dates.is_after_summer_b_start ?
                          'Summer Term B'
                          : 'Summer Term A')
                         : cur_qr)
                        : term);
        var quarter_str = (term === 'current' ?
                           cur_qr + ' quarter'
                           : (term.match(/^\d{4},[a-z]+$/) ?
                              term.replace(/\d{4},([a-z]+)/, '$1 quarter')
                              : term.replace(/\d{4},([a-z]+),([ab]-term)/, '$1 $2')));
        var source   = $("#card_with_no_course").html();
        var template = Handlebars.compile(source);
        var raw = template({term: term_str,
                            quarter: quarter_str});
        return raw;
    }
};
