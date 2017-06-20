var  SummaryScheduleCard = {
    name: 'SummaryScheduleCard',
    dom_target: undefined,
    term: 'current',
    course_error: null,
    instructed_course_error: null,

    render_init: function() {
        if (myuwFeatureEnabled('instructor_schedule')) {
            if (SummaryScheduleCard.term === 'current') {
                SummaryScheduleCard.term = window.term.year + ',' + window.term.quarter;
            }

            WSData.fetch_course_data_for_term(SummaryScheduleCard.term,
                                              SummaryScheduleCard.render_upon_data,
                                              SummaryScheduleCard.render_course_error);
            WSData.fetch_instructed_course_data_for_term(SummaryScheduleCard.term,
                                                         SummaryScheduleCard.render_upon_data,
                                                         SummaryScheduleCard.render_instructed_error);
        } else {
            $("#SummaryScheduleCard").hide();
        }
    },

    render_upon_data: function() {
        if (!SummaryScheduleCard._has_all_data()) {
            return;
        }

        SummaryScheduleCard._render();
        LogUtils.cardLoaded(SummaryScheduleCard.name, SummaryScheduleCard.dom_target);
    },

    render_instructed_error: function() {
        var error_code = WSData.instructed_course_data_error_code(SummaryScheduleCard.term);
        SummaryScheduleCard.instructed_course_error = error_code;
        if (SummaryScheduleCard.course_error) {
            SummaryScheduleCard.render_error();
        }
    },

    render_course_error: function() {
        var error_code = WSData.course_data_error_code(SummaryScheduleCard.term);
        SummaryScheduleCard.course_error = error_code;
        if (SummaryScheduleCard.instructed_course_error) {
            SummaryScheduleCard.render_error();
        }
    },

    render_error: function() {
        if (SummaryScheduleCard.course_error === 410 ||
            SummaryScheduleCard.instructed_course_error === 410) {
            Error410.render();
        } else if (SummaryScheduleCard.course_error === 404 &&
                   SummaryScheduleCard.instructed_course_error === 404) {
            $("#SummaryScheduleCard").hide();
        } else {
            raw = CardWithError.render("Summary Schedule");
            InstructorCourseCards.dom_target.html(raw);
        }
    },

    _has_all_data: function () {
        var instructed_course_data = WSData.normalized_instructed_course_data(SummaryScheduleCard.term);
        var course_data = WSData.normalized_course_data(SummaryScheduleCard.term);
        return (course_data || instructed_course_data);
    },

    _render: function () {
        var term = SummaryScheduleCard.term;
        var instructed_course_data = WSData.normalized_instructed_course_data(term);
        var course_data = WSData.normalized_course_data(SummaryScheduleCard.term);
        var source = $("#instructor_summary_schedule").html();
        var courses_template = Handlebars.compile(source);

        var raw = courses_template({
            quarter: (course_data) ? course_data.quarter: instructed_course_data.quarter,
            year: (course_data) ? course_data.year: instructed_course_data.year,
            course_data: course_data,
            instructed_course_data: instructed_course_data
        });

        SummaryScheduleCard.dom_target.html(raw);
        SummaryScheduleCard.add_events();
    },

    add_events: function(term) {
        $(".show_map").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_course_list_"+building, term);
        });
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.InstructorCourseCards = InstructorCourseCards;
