var CardWithNoCourse = {
    render: function( term ) {
        // If there's already a rendered no_course card,
        // don't draw a second one on the screen - MUWM-1924
        if ($(".no_courses_dupe_blocker").length) {
            return "";
        }
        var term_str = (term === 'current' ? 'Current Quarter' : titilizeTerm(term));
        var source   = $("#card_with_no_course").html();
        var template = Handlebars.compile(source);
        var raw = template({term: term_str});
        return raw;
    }
};
