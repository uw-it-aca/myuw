/*global $,Handlebars*/
var CourseListCard = {
    render_card: function (course_data) {
        var source,
            courses_template,
            index;
        for (index = 0; index < course_data.sections.length; index += 1) {
            course_data.sections[index].index = index;
            if (course_data.sections[index].class_website_url || course_data.sections[index].canvas_url) {
                course_data.sections[index].has_resources = true;
            }
        }
        source = $("#courses").html();
        courses_template = Handlebars.compile(source);

        $("body").on('shown.bs.collapse',
            function () {
                $(this).parent().find("div.accordion-footer > a > span.show_more").hide();
                $(this).parent().find("div.accordion-footer > a > span.show_less").show();
            });
        $("body").on('hidden.bs.collapse',
            function () {
                $(this).parent().find("div.accordion-footer > a > span.show_more").show();
                $(this).parent().find("div.accordion-footer > a > span.show_less").hide();
            });
//        }
        return courses_template(course_data);
    }
};
