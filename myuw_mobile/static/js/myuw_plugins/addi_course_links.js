(function( $ ){
    // This re-usable plugin displays
    // the additional course link panel
    // which has View Textbooks, Final exams, Other Quarters.

    $.fn.addi_course_links = function( inputs ) {  
        var settings = $.extend({}, {
            "registered_for_the_quarter": true,
            "visual": ""
	}, inputs);

	return this.each(function() {        
	    var source = $("#additional_course_links").html();
            var template = Handlebars.compile(source);
            $(this).html(template(settings));

            $(".show_textbooks").on("click", function(ev) {
		var hist = window.History;
		hist.pushState({
                    state: "textbooks",
		},  "", "/mobile/textbooks");
		return false;
            });

	    $(".show_finalexams").on("click", function(ev) {
		var hist = window.History;
		hist.pushState({
                    state: "final_exams" + settings.visual,
		},  "", "/mobile/final_exams" + settings.visual);
		return false;
            });

	    $(".show_other_quarters").on("click", function(ev) {
		var hist = window.History;
		hist.pushState({
                    state: "future_quarters" + settings.visual,
		},  "", "/mobile/future_quarters" + settings.visual);
		return false;
            });
	});
  };
})( jQuery );
