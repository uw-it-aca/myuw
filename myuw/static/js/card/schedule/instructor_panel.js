var CourseInstructorPanel = {

    render: function (c_section) {

        var source = $("#course_card_instructor_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#course_instructor' + c_section.index).html(raw);
    }
};
