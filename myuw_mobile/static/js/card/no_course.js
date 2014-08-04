var CardWithNoCourse = {
    render: function( term_str ) {
        var source   = $("#card_with_no_course").html();
        var template = Handlebars.compile(source);
        return template({term: term_str});
    },
};
