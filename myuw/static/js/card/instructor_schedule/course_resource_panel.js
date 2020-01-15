var InstructorCourseResourcePanel = {

    render: function (c_section) {
        var panel = $('#instructor_course_resource' + c_section.index);
        var term = c_section.year + ',' + c_section.quarter.toLowerCase();

        if (c_section.class_website_url ||
            c_section.canvas_url ||
            c_section.sln ||
            c_section.myuwclass_url) {
            c_section.display_resources = true;
        }

        Handlebars.registerPartial('course_class_list', $("#course_class_list").html());
        Handlebars.registerPartial('course_stats', $("#course_stats").html());
        Handlebars.registerPartial('class_website', $("#class_website").html());
        Handlebars.registerPartial('email_list', $("#email_list").html());
        Handlebars.registerPartial('online_tools', $("#online_tools").html());
        Handlebars.registerPartial('textbooks', $("#textbooks").html());
        var source = $("#instructor_course_resource_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        panel.html(raw);

        InstructorCourseResourcePanel.add_events(panel, term);
    },

    add_events: function(panel, term) {

        $(".myuwclass", panel).on("click", function(ev) {
            var target = ev.currentTarget;
            var course_id = safe_label(target.getAttribute("rel"));
            WSData.log_interaction("open_myuwclass_"+course_id, term);
        });

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
            var section_label = InstructorCourseResourcePanel.get_section_label(term, ev.currentTarget);
            label = safe_label(section_label);
            WSData.log_interaction("open_create_email_list_"+label);
            RequestEmailLists.render_init(section_label);
        });

        $(".manage_email_list", panel).on("click", function(ev) {
            var section_label = InstructorCourseResourcePanel.get_section_label(term, ev.currentTarget);
            var label = safe_label(section_label);
            WSData.log_interaction("open_manage_email_list_"+label);
            ManageEmailLists.render_init(section_label);
        });

        $(".download_classlist_csv", panel).on("click", function(ev) {
            var section_label = InstructorCourseResourcePanel.get_section_label(term, ev.currentTarget);

            var label = safe_label(section_label);
            WSData.log_interaction("download_course_classlist_"+label);
            PhotoClassList.download_class_list(section_label);
        });

        $(".course_class_list", panel).on("click", function(ev) {
            var section_label = ev.currentTarget.getAttribute("rel");
            window.open(ev.currentTarget.href, section_label);
            WSData.log_interaction("open_course_classlist_of_"+section_label);
            return false;
        });
    },

    get_section_label: function(term, target) {
        var section_label_parts = target.getAttribute("rel").split("_");
        var section_label = term + "," + section_label_parts[0] + "," + section_label_parts[1] + "/" + section_label_parts[2];
        return section_label;
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.InstructorCourseResourcePanel = InstructorCourseResourcePanel;
