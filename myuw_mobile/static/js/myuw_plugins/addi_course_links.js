(function( $ ){
    // This re-usable plugin displays
    // the additional course link panel
    // which has View Textbooks, Final exams, Other Quarters.

    $.fn.addi_course_links = function(inputs) {  
        var settings = $.extend({}, {
            registered_for_the_quarter: true
	}, inputs);

	return this.each(function() {        
	    var source = $("#additional_course_links").html();
            var template = Handlebars.compile(source);
            $(this).html(template(settings));

            $(".show_textbooks").bind("click", function(ev) {
		var hist = window.History;
		hist.pushState({
                    state: "textbooks",
		},  "", "/mobile/textbooks");
		return false;
            });

	    $(".show_finalexams").bind("click", function(ev) {
		var hist = window.History;
		hist.pushState({
                    state: "final_exams",
		},  "", "/mobile/final_exams");
		return false;
            });

	    $(".show_other_quarters").bind("click", function(ev) {
		var hist = window.History;
		hist.pushState({
                    state: "oquarters",
		},  "", "/mobile/oquarters");
		return false;
            });
	});
  };
})( jQuery );
