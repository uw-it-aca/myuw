var CourseResourcePanel = {

    render: function (c_section) {

        var source = $("#course_resource_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#course-resource' + c_section.index).html(raw);
    }
};
