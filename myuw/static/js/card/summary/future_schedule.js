var  FutureSummaryScheduleCard = {
    name: 'FutureSummaryScheduleCard',
    dom_target: undefined,
    term: undefined,

    hide_card: function() {
        if (window.user.instructor) {
            return false;
        }
        return true;
    },

    render_init: function() {
        if (FutureSummaryScheduleCard.hide_card()) {
            FutureSummaryScheduleCard.dom_target.hide();
            return;
        }

        if (!FutureSummaryScheduleCard.term || FutureSummaryScheduleCard.term === 'current') {
            FutureSummaryScheduleCard.term = window.term.next.year + ',' + window.term.next.quarter;
        }

        WSData.fetch_instructed_course_data_for_term(FutureSummaryScheduleCard.term,
                                                     FutureSummaryScheduleCard.render_upon_data,
                                                     FutureSummaryScheduleCard.render_error);
    },

    render_upon_data: function() {
        var inst_course_data = WSData._instructed_course_data[FutureSummaryScheduleCard.term];
        if (inst_course_data) {
            if (inst_course_data.sections.length === 0) {
                // if future term .sections.length is 0, hdie card
                $("#FutureSummaryScheduleCard").hide();
                return;
            }

            FutureSummaryScheduleCard._render();
            LogUtils.cardLoaded(FutureSummaryScheduleCard.name, FutureSummaryScheduleCard.dom_target);
        }
    },

    render_error: function() {
        var error_code = WSData.instructed_course_data_error_code(FutureSummaryScheduleCard.term);
        if (error_code === 410) {
            Error410.render();
            return;
        }
        if (error_code === 404) {
            $("#FutureSummaryScheduleCard").hide();
            return;
        }
        FutureSummaryScheduleCard._render_with_context({has_error: true});
    },

    _render_with_context: function(context){
        Handlebars.registerPartial('summary_section', $("#summary_section").html());
        Handlebars.registerPartial('summary_section_panel', $("#summary_section_panel").html());
        Handlebars.registerPartial('course_sche_col_days', $("#course_sche_col_days").html());
        Handlebars.registerPartial('course_sche_col_bldg', $("#course_sche_col_bldg").html());
        var source = $("#instructor_summary_schedule").html();
        var courses_template = Handlebars.compile(source);
        var raw = courses_template(context);
        FutureSummaryScheduleCard.dom_target.html(raw);
    },

    _render: function () {
        var term = FutureSummaryScheduleCard.term;
        var instructed_course_data = WSData.instructed_course_data(term, false);
        var data = {
            first_day_quarter: instructed_course_data.term.first_day_quarter,
            quarter: instructed_course_data.quarter,
            year: instructed_course_data.year,
            term: instructed_course_data.term,
            future_term: instructed_course_data.future_term,
            sections: instructed_course_data.sections,
            section_count: instructed_course_data.sections.length,
            show_enrollment: true
        };
        FutureSummaryScheduleCard._render_with_context(data);
        SummaryScheduleCard.add_events(term);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.FutureSummaryScheduleCard = FutureSummaryScheduleCard;
