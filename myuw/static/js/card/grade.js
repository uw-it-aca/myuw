var GradeCard = {
    name: 'GradeCard',
    dom_target: undefined,
    term: null,
    show_only_aterm: false,

    render_init: function() {
        if (!window.user.student) {
            $("#GradeCard").hide();
            return;
        }

        GradeCard.term = null;
        if (window.card_display_dates.is_after_last_day_of_classes) {
            GradeCard.term = 'current';

            if (window.card_display_dates.is_summer) {
                GradeCard.term = window.card_display_dates.current_summer_term;
            }
        }
        else if (window.card_display_dates.is_before_first_day_of_term) {
            // Fetch previous term's data...
            GradeCard.term = window.card_display_dates.last_term;
        }
        else if (window.card_display_dates.is_summer && window.card_display_dates.is_after_summer_b_start) {
            GradeCard.term = window.card_display_dates.current_summer_term;
            GradeCard.show_only_aterm = true;
        }

        if (GradeCard.term) {
            WSData.fetch_course_data_for_term(GradeCard.term, GradeCard.render_upon_data, GradeCard.render_error);
            return;
        }

        $("#GradeCard").hide();
    },

    render_upon_data: function() {
        if (!GradeCard._has_all_data()) {
            return;
        }
        GradeCard._render();
    },

    render_error: function() {
        var course_error_code = WSData.course_data_error_code(GradeCard.term);
        if (course_error_code === null || course_error_code === 404) {
            $("#GradeCard").hide();
            return;
        }
        GradeCard.dom_target.html(CardWithError.render("Final Grades"));
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
        var has_section_to_display = false;
        course_data.display_grade_card = true;
        course_data.display_grades = true;
        course_data.display_note = true;
        if (course_data.sections.length === 0) {
            course_data.display_grade_card = false;
        }
        if (window.card_display_dates.is_after_grade_submission_deadline) {
            course_data.display_note = false;
        }
        var index;
        // supporting MUWM-3014
        for (index = 0; index < course_data.sections.length; index += 1) {
            if (GradeCard.show_only_aterm && (course_data.sections[index].summer_term !== "A-term")) {
                course_data.sections[index].hide_for_early_summer_display = true;
                course_data.sections[index].display_grade = false;
            }
            if (course_data.sections[index].is_primary_section && !course_data.sections[index].is_auditor) {
                if (!course_data.sections[index].hide_for_early_summer_display) {
                    course_data.sections[index].display_grade = true;
                    has_section_to_display = true;
                }
            } else {
                course_data.sections[index].display_grade = false;
            }

            if (course_data.sections[index].grade === 'X') {
                course_data.sections[index].no_grade = true;
            } else {
                course_data.sections[index].no_grade = false;
            }
        }
        if (!has_section_to_display) {
            course_data.display_grade_card = false;
        }

        var source = $("#grade_card_content").html();
        var grades_template = Handlebars.compile(source);
        GradeCard.dom_target.html(grades_template(course_data));
        GradeCard.add_events(term);
        LogUtils.cardLoaded(GradeCard.name, GradeCard.dom_target);
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
