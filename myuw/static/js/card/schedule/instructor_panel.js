var CourseInstructorPanel = {

    render: function (c_section) {
        var i, ii;
        if (c_section.instructors && c_section.instructors.length > 0) {
            for (var i = 0; i < c_section.instructors.length; i++) {
                var instructor = c_section.instructors[i];

                if (instructor.addresses.length > 0) {
                    instructor.address1 = instructor.addresses[0];
                }

                if (instructor.email_addresses.length > 0) {
                    instructor.email1 = instructor.email_addresses[0];
                }

                if (instructor.phones.length > 0) {
                    instructor.phone1 = instructor.phones[0];
                    if (instructor.phones.length > 1) {
                        instructor.phone2 = instructor.phones[1];
                    }
                }

                if (instructor.positions.length > 0) {
                    for (ii = 0; ii < instructor.positions.length; ii++) {
                        if (instructor.positions[ii].is_primary ) {
                            instructor.title1 = instructor.positions[ii].title;
                            break;
                        }
                    }
                }
            }
        }
        var source = $("#course_card_instructor_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#course_instructor' + c_section.index).html(raw);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.CourseInstructorPanel = CourseInstructorPanel;
