var CourseModal = {
    show_course_modal: function(term, course_index) {
        var source   = $("#course_modal").html();
        var template = Handlebars.compile(source);

        var course_data;
        if (term) {
            WSData.normalize_instructors_for_term(term);
            course_data = WSData.course_data_for_term(term);
        }
        else {
            WSData.normalize_instructors();
            course_data = WSData.current_course_data(term);
        }
        var section = course_data.sections[course_index];

        if (section.class_website_url || section.canvas_url) {
            section.has_resources = true;
        }

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
            History.replaceState({
                state: "visual"
            },  "", "/mobile/visual");
        });

        $(".course_website").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id);
        });

        $(".show_map_modal").on("click", function(ev) {
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_course_modal_"+building);
        });


    }
};
 
