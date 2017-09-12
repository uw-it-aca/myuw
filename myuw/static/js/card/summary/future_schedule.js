var  FutureSummaryScheduleCard = {
    name: 'FutureSummaryScheduleCard',
    dom_target: undefined,
    term: undefined,

    hide_card: function() {
        if (myuwFeatureEnabled('instructor_schedule') &&
            window.user.instructor) {
            return false;
        }
        return true;
    },

    render_init: function() {
        if (FutureSummaryScheduleCard.hide_card()) {
            FutureSummaryScheduleCard.dom_target.hide();
            return;
        }

        if (FutureSummaryScheduleCard.term === 'current') {
            FutureSummaryScheduleCard.term = window.term.next.year + ',' + window.term.next.quarter;
        }

        WSData.fetch_instructed_course_data_for_term(FutureSummaryScheduleCard.term,
                                                     FutureSummaryScheduleCard.render_upon_data,
                                                     FutureSummaryScheduleCard.render_error);
    },

    render_upon_data: function() {
        var inst_course_data = WSData._instructed_course_data[FutureSummaryScheduleCard.term];
        if (inst_course_data) {
            FutureSummaryScheduleCard._render();
            LogUtils.cardLoaded(FutureSummaryScheduleCard.name, FutureSummaryScheduleCard.dom_target);
        }
    },

    render_error: function() {
        var error_code = WSData.instructed_course_data_error_code(FutureSummaryScheduleCard.term);
        if (error_code === 410) {
            Error410.render();
        } else if (error_code === 404) {
            $("#FutureSummaryScheduleCard").hide();
        } else {
            raw = CardWithError.render("FutureSummary Schedule");
            InstructorCourseCards.dom_target.html(raw);
        }
    },

    _render: function () {
        Handlebars.registerPartial('summary_section_panel', $("#summary_section_panel").html());

        var term = FutureSummaryScheduleCard.term;
        var instructed_course_data = WSData._link_secondary_sections(term);
        var source = $("#instructor_summary_schedule").html();
        var courses_template = Handlebars.compile(source);

        if (instructed_course_data.sections.length === 0 &&
           total_section_refs === 0) {
            $("#FutureSummaryScheduleCard").hide();
            return;
        }

        var data = {
            first_day_quarter: instructed_course_data.term.first_day_quarter,
            quarter: instructed_course_data.quarter,
            year: instructed_course_data.year,
            term: instructed_course_data.term,
            future_term: instructed_course_data.future_term,
            sections: instructed_course_data.sections,
            section_count: instructed_course_data.sections.length,
            hide_secondary: instructed_course_data.exceeded_max_display_sections,
            show_enrollment: true
        };
        var raw = courses_template(data);
        FutureSummaryScheduleCard.dom_target.html(raw);
        FutureSummaryScheduleCard.add_events();
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

            window.open(ev.target.href, '_blank', 'scrollbars=1,resizable=1,width='+width+',height='+height+',left='+left+',top='+top);

            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_classlist_"+course_id, term);
            return false;
        });

        $(".future-nav-link").click(function(ev) {
            var target = $(ev.target).attr('future-nav-target');
            WSData.log_interaction("view_instr_future_course_" + target);
        });

    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.FutureSummaryScheduleCard = FutureSummaryScheduleCard;
