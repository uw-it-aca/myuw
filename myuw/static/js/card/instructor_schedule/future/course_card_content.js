var InstructorFutureCourseCardContent = {

    render: function (c_section, fetched_eval) {
        var eval_data = (fetched_eval? WSData.iasystem_data(): null);
        var index = c_section.index;
        var source = $("#instructor_future_course_card_content_panel").html();
        var template = Handlebars.compile(source);

        var raw = template(c_section);
        $('#instructor_course_card_content' + index).html(raw);

        InstructorFutureCourseSchePanel.render(c_section);
        InstructorFutureCourseResourcePanel.render(c_section);

        if (c_section.grade_submission_delegates) {
            CourseInstructorPanel.render(c_section);
        }
    }
};
