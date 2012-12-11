var FinalsModal = {
    show_finals_modal: function(term, course_index) {
        var source   = $("#finals_modal").html();
        var template = Handlebars.compile(source);

        if (term) {
            WSData.normalize_instructors_for_term(term);
        }
        else {
            WSData.normalize_instructors_for_current_term();
        }
        var course_data;
        if (term) {
            course_data = WSData.course_data_for_term(term);
        }
        else {
            course_data = WSData.current_course_data();
        }
        var section = course_data.sections[course_index];

        var content = template(section);
        Modal.html(template(section));

        Modal.show();

        $('html,body').animate({scrollTop: 0}, 'fast');

        $(".instructor").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "instructor",
                instructor: ev.target.rel
            },  "", "/mobile/instructor/"+ev.target.rel);

            return false;
        });

        $(".close_modal").on("click", function() {
            if (term) {
                History.replaceState({
                    state: "final_exams",
                    term: term
                },  "", "/mobile/final_exams/"+term);
            }
            else {
                History.replaceState({
                    state: "final_exams"
                },  "", "/mobile/final_exams");
            }
        });

        $(".course_website").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id);
        });

        $(".show_map_modal").on("click", function(ev) {
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_final_modal_"+building);
        });
    }
};
 
