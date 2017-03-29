var InstructorCourseCards = {
    name: 'InstructorCourseCards',
    dom_target: undefined,
    term: 'current',

    render_init: function() {
        if (myuwFeatureEnabled('instructor_schedule')) {
            if (InstructorCourseCards.term === 'current') {
                InstructorCourseCards.term = window.term.year + ',' + window.term.quarter;
            }

            WSData.fetch_instructed_course_data_for_term(InstructorCourseCards.term,
                                                         InstructorCourseCards.render_upon_data,
                                                         InstructorCourseCards.render_error);
        } else {
            $("#InstructorCourseCards").hide();
        }
    },

    render_upon_data: function() {
        if (!InstructorCourseCards._has_all_data()) {
            return;
        }
        InstructorCourseCards._render();
        LogUtils.cardLoaded(InstructorCourseCards.name, InstructorCourseCards.dom_target);
    },

    render_error: function() {
        var error_code = WSData.instructed_course_data_error_code(InstructorCourseCards.term);
        if (error_code == 410) {
            Error410.render();
            return;
        }

        if (error_code === 404) {
            // no instructed courses found
            if ($('.instructed-terms').length) {
                var source = $("#instructor_course_card_no_courses").html();
                var courses_template = Handlebars.compile(source);
                $(".instructor_cards .card").remove();
                $(".instructor_cards").append(courses_template());
            } else {
                $("#InstructorCourseCards").hide();
            }
        } else {
            raw = CardWithError.render("Teaching Schedule");
            InstructorCourseCards.dom_target.html(raw);
        }
    },

    _has_all_data: function () {
        if (WSData.normalized_instructed_course_data(InstructorCourseCards.term)) {
            return true;
        }
        return false;
    },

    _render: function () {
        var term = InstructorCourseCards.term;
        var course_data = WSData.normalized_instructed_course_data(term);
        var source = $("#instructor_course_card_list").html();
        var courses_template = Handlebars.compile(source);
        var raw = courses_template(course_data);

        InstructorCourseCards.dom_target.html(raw);

        var course_sections = course_data.sections;
        $.each(course_sections, function () {
            this.year = course_data.year;
            this.quarter = course_data.quarter;
            this.summer_term = course_data.summer_term;
            if (course_data.future_term) {
                InstructorFutureCourseCardContent.render(this, null);
            } else if (course_data.past_term) {
                InstructorPastCourseCardContent.render(this, null);
            } else {
                InstructorCourseCardContent.render(this, null);
            }
        });

        InstructorCourseCards.add_events();
    },

    add_events: function() {
        $(".instructed-terms").change(function(ev) {
            InstructorCourseCards.term = $('.instructed-terms option:selected').val();
            InstructorCourseCards.render_init();
            WSData.log_interaction("show_instructed_courses_for_" + 
                                   InstructorCourseCards.term);
        });
    }
};
