var GradeCard = {
    name: 'GradeCard',
    dom_target: undefined,
    term: 'current',

    render_init: function() {
        if (window.card_display_dates.is_after_last_day_of_classes &&
            window.card_display_dates.is_before_first_day_of_current_term) {
            WSData.fetch_course_data_for_term(GradeCard.term, GradeCard.render_upon_data, GradeCard.render_error);
        }
        else {
            GradeCard.dom_target.hide();
        }
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
        course_data['display_note'] = true;
        if (course_data.sections.length == 0) {
            course_data['display_grade_card'] = false;
        }
        if (window.card_display_dates.is_after_grade_submission_deadline) {
            course_data['display_note'] = false;
        }
        var index;
        for (index = 0; index < course_data.sections.length; index += 1) {
            if (course_data.sections[index].grade === 'X') {
                course_data.sections[index]['no_grade'] = true;
            } else {
                course_data.sections[index]['no_grade'] = false;
            }
        }
        var source = $("#grade_card_content").html();
        var grades_template = Handlebars.compile(source);
        GradeCard.dom_target.html(grades_template(course_data));
        GradeCard.add_events(term);
    },

    add_events: function(term) {
        $("#toggle_grade_card_resources").on("click", function(ev) {
            ev.preventDefault();
            var card = $(ev.target).closest("[data-type='card']");
            $("#grade_card_resources").toggleClass("slide-show");

            if ($("#grade_card_resources").hasClass("slide-show")) {
                $("#toggle_grade_card_resources").text("SHOW LESS");
                $("#toggle_grade_card_resources").attr("title", "Hide additional grade resources");
                $("#grade_card_resources").attr("aria-hidden", "false");
                window.myuw_log.log_card(card, "expand");
            }
            else {
                $("#toggle_grade_card_resources").text("SHOW MORE");
                $("#toggle_grade_card_resources").attr("title", "Expand to show additional grade resources");
                $("#grade_card_resources").attr("aria-hidden", "true");
                window.myuw_log.log_card(card, "collapse");

                setTimeout(function() {
                    $("#toggle_grade_card_resources").text("SHOW MORE");
                }, 700);
            }
        });
        
    },
};
