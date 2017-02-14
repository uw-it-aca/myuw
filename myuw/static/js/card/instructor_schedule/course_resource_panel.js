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

        InstructorCourseResourcePanel.add_events(panel, term);
    },

    add_events: function(panel, term) {
        $(".course_website", panel).on("click", function(ev) {
            var target = ev.currentTarget;
            var course_id = safe_label(target.getAttribute("rel"));
            WSData.log_interaction("open_course_website_"+course_id, term);
        });

        $(".course_website_update", panel).on("click", function(ev) {
            var target = ev.currentTarget;
            var course_id = safe_label(target.getAttribute("rel"));
            WSData.log_interaction("update_course_website_"+course_id, term);
            window.open(target.getAttribute('data-href'),
                        'class_website_update',
                        'width=700,height=400');
        });

        $(".course_canvas_site", panel).on("click", function(ev) {
            var target = ev.currentTarget;
            course_id = safe_label(target.getAttribute("rel"));
            WSData.log_interaction("open_course_canvas_website_"+course_id, term);
        });

        $(".create_email_list", panel).on("click", function(ev) {
            var course_label = InstructorCourseResourcePanel.get_course_label(term, ev.currentTarget);
            label = safe_label(course_label);
            WSData.log_interaction("open_create_email_list_"+label, term);
            RequestEmailLists.render_init(course_label);
        });

        $(".manage_email_list", panel).on("click", function(ev) {
            var course_label = InstructorCourseResourcePanel.get_course_label(term, ev.currentTarget);
            label = safe_label(course_label);
            WSData.log_interaction("open_manage_email_list_"+label, term);
            ManageEmailLists.render_init(course_label);
        });

    },

    get_course_label: function(term, target) {
        var course_label_parts = target.getAttribute("rel").split("_");
        var course_label = term + "," + course_label_parts[0] + "," + course_label_parts[1] + "/" + course_label_parts[2];
        return course_label;
    }
};
