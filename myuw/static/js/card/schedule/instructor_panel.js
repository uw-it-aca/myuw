var CourseInstructorPanel = {

    render: function (c_section) {

        var source = $("#course_card_instructor_panel").html();
        var template = Handlebars.compile(source);
        $('#course_instructor' + c_section.index).html(template(c_section));
    }
};

 
