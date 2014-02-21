/*global $,Handlebars,gettext*/
var CourseListCard = {
    render_card: function (course_data, current_week) {
        var source,
            courses_template,
            index;
        for (index = 0; index < course_data.sections.length; index += 1) {
            course_data.sections[index].index = index;
            if (course_data.sections[index].class_website_url || course_data.sections[index].canvas_url) {
                course_data.sections[index].has_resources = true;
            }
        }

        switch (current_week) {
            case 1:
            case 2:
                source = $("#course_list_A").html();
                break;

            case 3:
            case 4:
            case 5:
            case 6:
            case 7:
            case 8:
                source = $("#course_list_B").html();
                break;

            case 9:
            case 10:
            case 11:
            case 12:
                source = $("#course_list_C").html();
                break;

            default:
                source = $("#courses").html();
                break;

        }
        courses_template = Handlebars.compile(source);

        $("body").on('shown.bs.collapse',
            function (event) {
                $(event.target).parent().find("div.accordion-footer > a > span.show_more").hide();
                $(event.target).parent().find("div.accordion-footer > a > span.show_less").show();
            });
        $("body").on('hidden.bs.collapse',
            function (event) {
                $(event.target).parent().find("div.accordion-footer > a > span.show_more").show();
                $(event.target).parent().find("div.accordion-footer > a > span.show_less").hide();
            });
        return courses_template(course_data);
    },
    init_events: function () {
        $('.canvasGradeBox').popover({content: gettext('canvas_grade_tip'),
                    selector: '.canvasGradeLabel',
                    placement: 'bottom'});
    }
};
