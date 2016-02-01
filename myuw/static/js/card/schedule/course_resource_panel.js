var CourseResourcePanel = {

    render: function (c_section) {

        var source = $("#course_resource_panel").html();
        var template = Handlebars.compile(source);
        $('#course-resource' + c_section.index).html(template(c_section));
    }
};
