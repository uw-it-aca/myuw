var CourseModal = {
    show_course_modal: function(course_index) {
        var source   = $("#course_modal").html();
        var template = Handlebars.compile(source);

        WSData.normalize_instructors();
        var course_data = WSData.course_data();
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
            History.replaceState({
                state: "visual"
            },  "", "/mobile/visual");
        });

        $(".course_website").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id);
        });
    }
};
 
