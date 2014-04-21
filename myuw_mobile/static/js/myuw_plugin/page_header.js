(function( $ ){
    // This re-usable plugin displays
    // the course list or vusual schedule page header panel

    $.fn.page_header = function( inputs ) {
        var settings = $.extend( {
            "quarter" : "",
            "year" : "",
            "view_name" : "",  // such as: Courses, Final Exams, Textbooks
            "summer_term": "", // such as: A-term, B-term
            "on_current_list": false,
            "on_current_visual": false,
            "on_future_list": false,
            "on_future_visual": false
        }, inputs);

        return this.each(function() {
            var source   = $("#page_header").html();
            var template = Handlebars.compile(source);
            $(this).html(template(settings));
        });
    };
})( jQuery );
