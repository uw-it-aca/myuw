var CourseCardHiddenPanel = {

    render: function (c_section) {
        var source = $("#course_card_hidden_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#hidden_content_on_course_card' + c_section.index).html(raw);

        CourseSchePanel.render(c_section);

        CourseResourcePanel.render(c_section);

        if (c_section.instructors) {
            CourseInstructorPanel.render(c_section);
        }
    }
};
