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
        $("#main-content").html(template({terms: grouped}));
    },

    group_events_by_term: function(events) {
        var groups = [];
        var current_term = "";
        for (var i = 0; i < events.length; i++) {
            var ev = events[i];

            var term_name = ev.year + " " + ev.quarter;

            if (term_name != current_term) {
                current_term = term_name;
                groups.push({
                    year: ev.year,
                    quarter: ev.quarter,
                    events: []
                });
            }

            groups[groups.length-1].events.push(ev);
        }

        return groups;
    }
};
