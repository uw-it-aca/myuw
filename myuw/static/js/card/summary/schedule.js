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
        var instructed_course_data = WSData.instructed_course_data(term, false);
        var source = $("#instructor_summary_schedule").html();
        var courses_template = Handlebars.compile(source);
        var data = {
            first_day_quarter: instructed_course_data.term.first_day_quarter,
            quarter: instructed_course_data.quarter,
            year: instructed_course_data.year,
            future_term: instructed_course_data.future_term,
            sections: instructed_course_data.sections,
            section_count: instructed_course_data.sections.length
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
            var section_label = ev.currentTarget.getAttribute("rel");
            window.open(ev.currentTarget.href, section_label);
            WSData.log_interaction("from_summary_open_course_classlist_of_" + section_label, term);
            return false;
        });

        $(".pin_mini_card_" + term_id).on("click", function(ev) {
            ev.preventDefault();
            var section_abbr = ev.currentTarget.getAttribute("cabb");
            var course_number = ev.currentTarget.getAttribute("cnum");
            var section_id = ev.currentTarget.getAttribute("sid");
            var label = safe_label(section_abbr) + "_" + course_number + "_" + section_id;
            WSData.log_interaction("from_summary_pin_mini_card_of_" + label, term);
            var section_label = (term + "," + section_abbr + "," +
                                 course_number + "/" + section_id);
            $.ajax({
                url: "/api/v1/inst_section_display/" + section_label + "/pin_mini",
                dataType: "JSON",
                async: true,
                type: 'GET',
                accepts: {html: "text/html"},
                success: function(results) {
                    if (results.done) {
                        window.location = ev.currentTarget.href;
                    }
                },
                error: function(xhr, status, error) {
                    return false;
                }
            });
        });
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.SummaryScheduleCard = SummaryScheduleCard;
