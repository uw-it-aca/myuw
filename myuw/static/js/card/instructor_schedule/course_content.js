var InstructorCourseCardContent = {

    render: function (c_section) {
        Handlebars.registerPartial('secondary_section_panel', $("#secondary_section_panel").html());
        Handlebars.registerPartial('course_sche_col_days', $("#course_sche_col_days").html());
        Handlebars.registerPartial('course_sche_col_bldg', $("#course_sche_col_bldg").html());
        Handlebars.registerPartial('course_grading', $("#course_grading").html());
        Handlebars.registerPartial('course_eval', $("#course_eval").html());
        Handlebars.registerPartial('secondaries', $("#secondaries").html());
        Handlebars.registerPartial('secondary_section_panel', $("#secondary_section_panel").html());
        var index = c_section.index;
        var source = $("#instructor_course_card_content_panel").html();
        var template = Handlebars.compile(source);
        var card = $('#instructor_course_card_content' + index);
        var quarter = c_section.quarter.toLowerCase();
        if (c_section.is_primary_section && c_section.final_exam &&
            !c_section.final_exam.no_exam_or_nontraditional &&
            !c_section.final_exam.is_confirmed && c_section.sln) {
            if (quarter === 'summer') {
                c_section.final_exam.display_no_final_period = true;
            } else {
                if(c_section.course_campus === "Seattle"){
                    c_section.display_confirm_final_link = true;
                }
            }
        }
        var raw = template(c_section);
        card.html(raw);

        InstructorCourseSchePanel.render(c_section);
        InstructorCourseResourcePanel.render(c_section);

        if (c_section.grade_submission_delegates) {
            CourseInstructorPanel.render(c_section);
        }

        var term = c_section.year + ',' + quarter;
        InstructorCourseCardContent.add_events(card, term);
    },

    add_events: function(card, term) {

        $(".show_map", card).on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_course_list_"+building, term);
        });
        $(".course_delegate_link", card).on("click", function(ev) {
            var width = 800;
            var height = 400;

            var left = window.screenX + 200;
            var top = window.screenY + 200;

            window.open(ev.currentTarget.href, '_blank', 'width='+width+',height='+height+',left='+left+',top='+top);

            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_delegate__"+course_id, term);
            return false;
        });
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.InstructorCourseCardContent = InstructorCourseCardContent;
