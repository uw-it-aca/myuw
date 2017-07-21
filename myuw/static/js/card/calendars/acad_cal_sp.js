var AcadCalSnippet = {
    name: 'AcadCalSnippet',
    dom_target: undefined,

    render_init: function() {
        AcadCalSnippet.dom_target  = $('#AcadCalSnippet');
        if (!window.user.instructor) {
            AcadCalSnippet.dom_target.hide();
            return;
        }
        WSData.fetch_current_academic_calendar_events(AcadCalSnippet.render);
    },

    render: function () {
        var calendar_data = WSData.current_academic_calendar_data();

        if (calendar_data.length > 0) {
            var source = $("#calendar_snippet").html();
            var template = Handlebars.compile(source);

            var events = AcadCalSnippet.refine_event_fields(calendar_data);
            var html = template({events: events});
            AcadCalSnippet.dom_target.html(html);
        }
    },

    refine_event_fields: function(events) {
        var i;
        for (i = 0; i < events.length; i++) {
            var ev = events[i];
            if (ev.is_all_day) {
                delete(ev.end);
            }
        }
        return events;
    },

    filter_events: function(events) {
        // Sort by date and then by name
        events = events.sort(function(a, b) {
            if (!a.start_date) {
                a.start_date = new Date(a.start);
                a.end_date = new Date(a.end);
            }
            if (!b.start_date) {
                b.start_date = new Date(b.start);
                b.end_date = new Date(b.end);
            }

            if (a.start_date > b.start_date) {
                return 1;
            }
            if (b.start_date > a.start_date) {
                return -1;
            }

            if (a.summary > b.summary) {
                return 1;
            }
            if (b.summary > a.summary) {
                return -1;
            }
            return 0;
        });

        return events.slice(0, 3);
    }
};
