var GradeCard = {
    name: 'GradeCard',
    dom_target: undefined,
    term: 'current',

    render_init: function() {
        WSData.fetch_course_data_for_term(GradeCard.term, GradeCard.render_upon_data, GradeCard.render_error);
    },

    render_upon_data: function() {
        if (!GradeCard._has_all_data()) {
            return;
        }
        GradeCard._render();
    },

    render_error: function() {
        GradeCard.dom_target.html(CardWithNoCourse.render(titilizeTerm(GradeCard.term)));
    },

    _has_all_data: function () {
        if (WSData.normalized_course_data(GradeCard.term)) {
            return true;
        }
        return false;
    },

    _render: function () {
        var term = GradeCard.term;
        var course_data = WSData.normalized_course_data(term);
        course_data['display_grade_card'] = true;
        course_data['display_grades'] = true;
        if (course_data.sections.length == 0) {
            course_data['display_grade_card'] = false;
        }
        var source = $("#grade_card_content").html();
        var grades_template = Handlebars.compile(source);
        GradeCard.dom_target.html(grades_template(course_data));
        GradeCard.add_events(term);
    },

    add_events: function(term) {
        $("#toggle_grade_card_resources").on("click", function(ev) {
            ev.preventDefault();
            $("#grade_card_resources").toggleClass("slide-show");

            if ($("#grade_card_resources").hasClass("slide-show")) {
                $("#toggle_grade_card_resources").text("SHOW LESS");
                $("#toggle_grade_card_resources").attr("title", "Hide additional grade resources");
                $("#grade_card_resources").attr("aria-hidden", "false");
                WSData.log_interaction("show_grade_card_resources");
            }
            else {
                $("#toggle_grade_card_resources").text("SHOW MORE");
                $("#toggle_grade_card_resources").attr("title", "Expand to show additional grade resources");
                $("#grade_card_resources").attr("aria-hidden", "true");

                setTimeout(function() {
                    $("#toggle_grade_card_resources").text("SHOW MORE");
                }, 700);
            }
        });
        
    },
};
