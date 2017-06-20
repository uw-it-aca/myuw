var  SummaryScheduleCard = {
    name: 'SummaryScheduleCard',
    dom_target: undefined,
    term: 'current',

    render_init: function() {
        if (myuwFeatureEnabled('instructor_schedule')) {
            if (SummaryScheduleCard.term === 'current') {
                SummaryScheduleCard.term = window.term.year + ',' + window.term.quarter;
            }

            WSData.fetch_instructed_course_data_for_term(SummaryScheduleCard.term,
                                                         SummaryScheduleCard.render_upon_data,
                                                         SummaryScheduleCard.render_error);
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

                $("div[data-tab-type='instructor-term-nav']").removeClass("myuw-tab-selected");
                $("div[data-tab-type='instructor-term-nav'][data-term='"+InstructorCourseCards.term+"']").addClass("myuw-tab-selected");
                $("#teaching-term-select option[value='"+InstructorCourseCards.term+"']").prop('selected', true);
                InstructorCourseCards._show_correct_term_dropdown();

            } else {
                $("#InstructorCourseCards").hide();
            }
        } else {
            raw = CardWithError.render("Teaching Schedule");
            InstructorCourseCards.dom_target.html(raw);
        }
    },

    _has_all_data: function () {
        if (WSData.normalized_instructed_course_data(SummaryScheduleCard.term)) {
            return true;
        }
        return false;
    },

    _render: function () {
        var term = SummaryScheduleCard.term;
        var course_data = WSData.normalized_instructed_course_data(term);
        var source = $("#instructor_summary_schedule").html();
        var courses_template = Handlebars.compile(source);

        var raw = courses_template(course_data);
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
