var  SummaryScheduleCard = {
    name: 'SummaryScheduleCard',
    dom_target: undefined,
    term: 'current',

    render_init: function() {
        if (myuwFeatureEnabled('instructor_schedule') && window.user.instructor) {
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
        var error_code = WSData.instructed_course_data_error_code(SummaryScheduleCard.term);
        if (error_code === 410) {
            Error410.render();
        } else if (error_code === 404) {
            $("#SummaryScheduleCard").hide();
        } else {
            raw = CardWithError.render("Summary Schedule");
            InstructorCourseCards.dom_target.html(raw);
        }
    },

    _has_all_data: function () {
        return WSData.normalized_instructed_course_data(SummaryScheduleCard.term) !== undefined;
    },

    _render: function () {
        var term = SummaryScheduleCard.term;
        var instructed_course_data = WSData.normalized_instructed_course_data(term);
        var source = $("#instructor_summary_schedule").html();
        var courses_template = Handlebars.compile(source);

        var raw = courses_template({
            quarter: instructed_course_data.quarter,
            year: instructed_course_data.year,
            sections: instructed_course_data.sections,
            is_instructor: (instructed_course_data !== undefined)
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

        $(".course_class_list").on("click", function(ev) {
            var width = 800;
            var height = 400;

            var left = window.screenX + 200;
            var top = window.screenY + 200;

            window.open(ev.target.href, '_blank', 'width='+width+',height='+height+',left='+left+',top='+top);

            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_classlist_"+course_id, term);
            return false;
        });
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.InstructorCourseCards = InstructorCourseCards;
