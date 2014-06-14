var NoCourse = {
    render: function( quarter_or_term_str ) {
        var source   = $("#card_with_no_course").html();
        var template = Handlebars.compile(source);
        return template({quarter_or_term: quarter_or_term_str});
    },
};
