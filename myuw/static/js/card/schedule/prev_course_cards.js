var PrevTermCourseCards = {
    name: 'PrevTermCourseCards',
    dom_target: undefined,
    term: undefined,

    render_init: function() {
        PrevTermCourseCards.term = "prev_unfinished";
        PrevTermCourseCards.dom_target = $("#PrevTermCourseCards");
        if (!window.user.student) {
            $("#PrevTermCourseCards").hide();
            return;
        }
        WSData.fetch_course_data_for_term(PrevTermCourseCards.term, PrevTermCourseCards.render_upon_data, PrevTermCourseCards.render_error);
    },

    render_upon_data: function() {
        if (!PrevTermCourseCards._has_all_data()) {
            return;
        }
        PrevTermCourseCards._render();
        LogUtils.cardLoaded(PrevTermCourseCards.name, PrevTermCourseCards.dom_target);
    },

    _has_all_data: function () {
        if (WSData.course_data_for_term(PrevTermCourseCards.term)) {
            return true;
        }
        return false;
    },

    render_error: function() {
        var error_code = WSData.course_data_error_code(PrevTermCourseCards.term);
        if (error_code === 404) {
            $("#PrevTermCourseCards").hide();
            return false;
        }
        CardWithError.render("Previous Unfinished Course Info");
        PrevTermCourseCards.dom_target.html(raw);
        return true;
    },

    _render: function () {
        var results = WSData.course_data_for_term(PrevTermCourseCards.term);
        for (i = 0; i < results.length; i++) {
            var term_course_data = results[i];
            WSData.process_term_course_data(term_course_data);
            WSData._normalize_instructors(term_course_data);
            var term_label = term_course_data.term.label.replace(/,/g, '_');
            var course_sections = term_course_data.sections;
            for (index = 0; index < course_sections.length; index++) {
                section = course_sections[index];
                section.index = term_label + '_' + section.index;
                section.year = term_course_data.year;
                section.quarter = term_course_data.quarter;
                section.summer_term = term_course_data.summer_term;
            }

            term_course_data.display_term = true;
            var source = $("#course_card_list").html();
            var courses_template = Handlebars.compile(source);
            var raw = courses_template(term_course_data);
            PrevTermCourseCards.dom_target.html(raw);

            for (index = 0; index < course_sections.length; index++) {
                CourseCardContentPanel.render(course_sections[index], false);
            }

            CourseCards.add_events(term_label);
        }
    },
};
