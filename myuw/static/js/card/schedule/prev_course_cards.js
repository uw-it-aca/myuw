var PrevTermCourseCards = {
    name: 'PrevTermCourseCards',
    dom_target: undefined,
    term: undefined,

    hide_card: function() {
        if (window.user.pce) {
            return false;
        }
        return true;
    },

    render_init: function() {
        PrevTermCourseCards.term = "prev_unfinished";
        PrevTermCourseCards.dom_target = $("#PrevTermCourseCards");
        if (PrevTermCourseCards.hide_card()) {
            $("#PrevTermCourseCards").hide();
            $("#PrevTermCourseCards1").hide();
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
        $("#PrevTermCourseCards1").hide();
        if (error_code === 404) {
            PrevTermCourseCards.dom_target.hide();
            return false;
        }
        CardWithError.render("Previous Unfinished Course Info");
        PrevTermCourseCards.dom_target.html(raw);
        return true;
    },

    _render: function () {
        var results = WSData.course_data_for_term(PrevTermCourseCards.term);
        if (results.length === 1) {
            $("#PrevTermCourseCards1").hide();
        }
        for (i = 0; i < results.length; i++) {
            var term_course_data = results[i];
            WSData.process_term_course_data(term_course_data);
            WSData._normalize_instructors(term_course_data);
            var term_label = term_course_data.term.label.replace(/,/g, '_');
            var quarter = term_course_data.quarter;
            var course_sections = term_course_data.sections;
            for (index = 0; index < course_sections.length; index++) {
                section = course_sections[index];
                section.index += term_label;
                section.year = term_course_data.year;
                section.quarter = quarter;
            }

            term_course_data.display_term = true;
            var source = $("#course_card_list").html();
            var courses_template = Handlebars.compile(source);
            var raw = courses_template(term_course_data);
            if (i > 0) {
                PrevTermCourseCards.dom_target = $("#PrevTermCourseCards1");
            }
            PrevTermCourseCards.dom_target.html(raw);

            for (index = 0; index < course_sections.length; index++) {
                CourseCardContentPanel.render(course_sections[index], false);
            }
            LoadCourseEval.add_events(quarter);
            CourseCards.add_events(term_label);
        }
    },
};

var PrevTermCourseCards1 = {
    name: 'PrevTermCourseCards1',
    render_init: function() {}
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.PrevTermCourseCards = PrevTermCourseCards;
exports.PrevTermCourseCards1 = PrevTermCourseCards1;
