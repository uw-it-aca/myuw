var AcademicCalendar = {
    show_events: function() {
        "use strict";
        CommonLoading.render_init();
        WSData.fetch_academic_calendar_events(AcademicCalendar.render_events);
    },

    render_events: function() {
        "use strict";
        var events = WSData.academic_calendar_data();

        var source = $("#calendar_events").html();
        var template = Handlebars.compile(source);
        var grouped = AcademicCalendar.group_events_by_term(events);
        var sorted = grouped.sort(AcademicCalendar.term_sort);
        $("#main-content").html(template({terms: sorted}));

        AcademicCalendar.add_events();
    },

    term_sort: function(term_a, term_b){
        var a_year = parseInt(term_a.year),
            b_year = parseInt(term_b.year),
            term_order = ["winter", "spring", "summer", "autumn"];
        if(a_year != b_year) {
            return a_year > b_year ? 1 : -1;
        }
        if(term_a.quarter != term_b.quarter){
            return term_order.indexOf(term_a.quarter.toLowerCase()) > term_order.indexOf(term_b.quarter.toLowerCase()) ? 1 : -1;
        }
        return 0;

    },

    group_events_by_term: function(events) {
        var groups = [];
        var current_term = "";

        var by_group = {};
        for (var i = 0; i < events.length; i++) {
            var ev = events[i];

            var term_name = ev.year + " " + ev.quarter;
            var group_name = term_name;
            var new_group = {
                year: ev.year,
                quarter: ev.quarter,
                events: []
            };

            if (ev.myuw_categories.term_breaks) {
                group_name = group_name+"-break";
                new_group.term_break = true;

                by_group[group_name] = new_group;
                groups.push(new_group);
            }
            else if (!by_group.hasOwnProperty(group_name)) {
                current_term = term_name;

                by_group[group_name] = new_group;
                groups.push(new_group);
            }

            by_group[group_name].events.push(ev);
        }

        return groups;
    },

    filter_all: function() {
        $(".myuw-selected-button").removeClass("myuw-selected-button");
        $("#myuw-event-filter-all").addClass("myuw-selected-button");
        $(".acal-page-event").show();
    },
    filter_breaks: function() {
        $(".myuw-selected-button").removeClass("myuw-selected-button");
        $("#myuw-event-filter-breaks").addClass("myuw-selected-button");
        $(".acal-page-event").hide();
        $(".acal-page-event-break").show();
    },
    filter_classes: function() {
        $(".myuw-selected-button").removeClass("myuw-selected-button");
        $("#myuw-event-filter-classes").addClass("myuw-selected-button");
        $(".acal-page-event").hide();
        $(".acal-page-event-class").show();
    },

    add_events: function() {
        $("#myuw-event-filter-all").click(AcademicCalendar.filter_all);
        $("#myuw-event-filter-breaks").click(AcademicCalendar.filter_breaks);
        $("#myuw-event-filter-classes").click(AcademicCalendar.filter_classes);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.AcademicCalendar = AcademicCalendar;
