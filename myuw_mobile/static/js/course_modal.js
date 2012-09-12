var CourseModal = {
    show_course_modal: function(course_index) {
        var source   = $("#course_modal").html();
        var template = Handlebars.compile(source);

        WSData.normalize_instructors();
        var course_data = WSData.course_data();
        var section = course_data.sections[course_index];

        var content = template(section);
        $("#page-modal").html(template(section));

        CourseModal.show_modal();
        $('html,body').animate({scrollTop: 0}, 'fast');

        $(".close").on("click", function() {
            CourseModal.close_modal();
        });
    },

    close_modal: function() {
        $("#page-modal").hide();
        $("#page-content").show();
    },

    show_modal: function() {
        $("#page-content").hide();
        $("#page-modal").show();
    }
};
 
