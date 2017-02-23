var InstructorPastCourseSchePanel = {

    render: function (c_section) {
        var source = $("#instructor_past_course_sche_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#instructor_sche_on_course_card' + c_section.index).html(raw);
    }
};
