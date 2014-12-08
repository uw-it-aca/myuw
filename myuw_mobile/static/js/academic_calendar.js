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
        $("#main-content").html(template({events: events}));
    }
};
