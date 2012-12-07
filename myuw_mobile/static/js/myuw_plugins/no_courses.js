(function( $ ){
    // This re-usable plugin displays
    // the no credit course registered message panel

    $.fn.no_courses = function(inputs) {
        var settings = $.extend({}, {
            which_quarter_or_term : 'this quarter'
        }, inputs);

        return this.each(function() {
            var source   = $("#no-courses").html();
            var template = Handlebars.compile(source);
	    Handlebars.registerPartial("no-course-msg", 
				       $("#no-course-msg").html());
            $(this).html(template(settings));
	    
	    $("#addi_links").addi_course_links({
		'registered_for_the_quarter' : false });
        });
    };
})( jQuery );
