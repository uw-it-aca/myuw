var SummaryScheduleCard = {
    name: 'SummaryScheduleCard',
    dom_target: undefined,
    term: undefined,

    hide_card: function() {
        if (window.user.instructor) {
            return false;
        }
        return true;
    },

    render_init: function() {
        if (SummaryScheduleCard.hide_card()) {
            $("#SummaryScheduleCard").hide();
            return;
        }

        if (!SummaryScheduleCard.term || SummaryScheduleCard.term === 'current') {
            SummaryScheduleCard.term = window.term.year + ',' + window.term.quarter;
        }

        WSData.fetch_instructed_course_data_for_term(SummaryScheduleCard.term,
                                                     SummaryScheduleCard.render_upon_data,
                                                     SummaryScheduleCard.render_error);
    },

    render_upon_data: function() {
        var inst_course_data = WSData._instructed_course_data[SummaryScheduleCard.term];
        if (inst_course_data) {
            // if .sections.length is 0, display msg
            SummaryScheduleCard._render();
            LogUtils.cardLoaded(SummaryScheduleCard.name, SummaryScheduleCard.dom_target);
        }
    },

    render_error: function() {
        var error_code = WSData.instructed_course_data_error_code(SummaryScheduleCard.term);
        if (error_code === 410) {
            Error410.render();
            return;
        }
        if (error_code === 404) {
            $("#SummaryScheduleCard").hide();
            return;
        }
        var raw = CardWithError.render("Schedule Summary");
        InstructorCourseCards.dom_target.html(raw);
    },

    _render: function () {
        Handlebars.registerPartial('summary_section_panel', $("#summary_section_panel").html());
        var term = SummaryScheduleCard.term;
        var instructed_course_data = WSData._link_secondary_sections(term);
        var source = $("#instructor_summary_schedule").html();
        var courses_template = Handlebars.compile(source);
        var data = {
            first_day_quarter: instructed_course_data.term.first_day_quarter,
            quarter: instructed_course_data.quarter,
            year: instructed_course_data.year,
            future_term: instructed_course_data.future_term,
            sections: instructed_course_data.sections,
            section_count: instructed_course_data.sections.length,
            hide_secondary: instructed_course_data.exceeded_max_display_sections
        };
        var raw = courses_template(data);
        SummaryScheduleCard.dom_target.html(raw);
        SummaryScheduleCard.add_events(term);
    },

    add_events: function(term) {
        var term_id = term.replace(',', '_');

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
/*
        $(".toggle_secondary_" + term_id).on("click", function(ev) {
            ev.preventDefault();
            var card = $(ev.target).closest("[data-type='card']");
            var item_id = this.getAttribute("aria-controls");
            var div = $("#" + item_id);
            var expose = $("#show_" + item_id + "_wrapper");
            var hide = $("#hide_"  + item_id + "_wrapper");
            toggle_card_disclosure(card, div, expose, hide, item_id);
        });
        */
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.SummaryScheduleCard = SummaryScheduleCard;
