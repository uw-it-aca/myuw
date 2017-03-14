var InstructorFutureCourseResourcePanel = {

    render: function (c_section) {
        if (c_section.class_website_url || c_section.canvas_url) {
            c_section.has_resources = true;
        }

        var source = $("#instructor_future_course_resource_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#instructor_course_resource' + c_section.index).html(raw);
    }
};
