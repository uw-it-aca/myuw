var InstructorCourseResourcePanel = {

    render: function (c_section) {
        var panel = $('#instructor_course_resource' + c_section.index);
        var term = c_section.year + ',' + c_section.quarter.toLowerCase();

        if (c_section.class_website_url || c_section.canvas_url) {
            c_section.has_resources = true;
        }

        var source = $("#instructor_course_resource_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        panel.html(raw);

        InstructorCourseResourcePanel.add_events(panel);
    },

    add_events: function(panel, term) {
        $(".course_website", panel).on("click", function(ev) {
            var target = ev.currentTarget;
            var course_id = target.getAttribute("rel").replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id, term);
        });

        $(".course_website_update", panel).on("click", function(ev) {
            var target = ev.currentTarget;
            var course_id = target.getAttribute("rel").replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("update_course_website_"+course_id, term);
            window.open(target.getAttribute('data-href'),
                        'class_website_update',
                        'width=700,height=400');
        });

        $(".course_canvas_site", panel).on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_canvas_website_"+course_id, term);
        });
    }
};
