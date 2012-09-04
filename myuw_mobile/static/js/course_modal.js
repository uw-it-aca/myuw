var CourseModal = {
    show_course_modal: function(course_index) {
        var source   = $("#course_modal").html();
        var template = Handlebars.compile(source);

        var course_data = WSData.course_data();
        var section = course_data.sections[course_index];

        var content = template(section);
        $("#course_modal_dialog").html(template(section));
        $("#course_modal_dialog").modal('show');

        $(".close_modal").on("click", function() {
            $("#course_modal_dialog").modal('hide');
        });
    }
};
 
