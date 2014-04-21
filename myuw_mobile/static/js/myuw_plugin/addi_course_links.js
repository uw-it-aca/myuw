(function( $ ){
    // This re-usable plugin displays
    // the additional course link panel
    // which has View Textbooks, Final exams, Other Quarters.

    $.fn.addi_course_links = function( inputs ) {  
        var settings = $.extend({}, {
            registered_for_the_quarter: true,
            show_future_link: true,
            visual: "",
            term: ""
        }, inputs);

        return this.each(function() {        
            var source = $("#additional_course_links").html();
            var template = Handlebars.compile(source);
            $(this).html(template(settings));

            $(".show_textbooks").on("click", function(ev) {
                WSData.log_interaction((settings.visual?"visual_schedule":"course_list")+"_view_textbooks", settings.term);
                var hist = window.History;
                if (settings.term) {
                    hist.pushState({
                        state: "textbooks",
                        term: settings.term
                    },  "", "/mobile/textbooks/"+settings.term);
                }
                else {
                    hist.pushState({
                        state: "textbooks"
                    },  "", "/mobile/textbooks");
                }
                return false;
            });

            $(".show_finalexams").on("click", function(ev) {
                WSData.log_interaction((settings.visual?"visual_schedule":"course_list")+"_view_finalexams", settings.term);
                var hist = window.History;
                if (settings.term) {
                    hist.pushState({
                        state: "final_exams",
                        term: settings.term
                    },  "", "/mobile/final_exams/"+settings.term);
                }
                else {
                    hist.pushState({
                        state: "final_exams"
                    },  "", "/mobile/final_exams");
                }
                return false;
            });

            if (settings.show_future_link) {
                $(".show_other_quarters").on("click", function(ev) {
                    var hist = window.History;
                    hist.pushState({
                        state: "future_quarters"
                    },  "", "/mobile/future_quarters" + settings.visual);
                    return false;
                });
            }
        });
  };
})( jQuery );
