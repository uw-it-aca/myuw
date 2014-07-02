var CourseCard = {

    render_init: function(term, course_index) {
        var course_data =  WSData.normalized_course_data(term);
        if (course_data === undefined) {
            $("#course_card_row").html(CardLoading.render("Course List"));
            return;
        }
        CourseCard.render(course_data, term, course_index);
    },

    render_upon_data: function (course_data, term, course_index) {
        if (course_data === undefined) {
            $("#course_card_row").html(CardWithError.render());
            return;
        }
        CourseCard.render(course_data, term, course_index);
    },

    render: function (course_data, term, course_index) {
        if (course_data.sections.length == 0) {
            $("#course_card_row").html(CardWithNoCourse.render("this quarter"));
            return;
        }

        var index;
        for (index = 0; index < course_data.sections.length; index += 1) {
            course_data.sections[index].index = index;
            if (course_data.sections[index].class_website_url || course_data.sections[index].canvas_url) {
                course_data.sections[index].has_resources = true;
            }
        }
        var source = $("#course_card_content").html();
        var courses_template = Handlebars.compile(source);

        $("body").on('shown.bs.collapse', function (event) {
            $(event.target).parent().find("div.accordion-footer > a > span.show_more").hide();
            $(event.target).parent().find("div.accordion-footer > a > span.show_less").show();
        });
        
        $("body").on('hidden.bs.collapse', function (event) {
            $(event.target).parent().find("div.accordion-footer > a > span.show_more").show();
            $(event.target).parent().find("div.accordion-footer > a > span.show_less").hide();
        });

        $("#course_card_row").html(courses_template(course_data));
        CourseCard.add_events(term);
    },

    add_events: function(term) {
        $('.canvasGradeBox').popover({content: gettext('canvas_grade_tip'),
                                      selector: '.canvasGradeLabel',
                                      placement: 'bottom'});
    },
};
