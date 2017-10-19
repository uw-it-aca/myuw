var AcademicCalendarCard = {
    name: 'AcademicCalendarCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_academic_calendar_events(AcademicCalendarCard.render);
    },

    render: function() {
        var events = WSData.academic_calendar_data();
        var source = $("#calendar_events").html();
        var template = Handlebars.compile(source);
        var grouped = AcademicCalendarCard.group_events_by_term(events);
        AcademicCalendarCard.dom_target.html(template({terms: grouped}));

        LogUtils.cardLoaded(AcademicCalendarCard.name, AcademicCalendarCard.dom_target);

        AcademicCalendarCard.add_events();
        if (window.location.hash) {
            var l = $('a[name="' +
                      window.location.hash.substr(1).replace(/-/g, ' ') +
                      '"]');
            if (l.length) {
                setTimeout(function () {
                    $('html,body').animate({scrollTop: l.offset().top},'slow');
                }, 250);
            }
        }
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
            else if (term_name != current_term) {
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
        $("#myuw-event-filter-all").attr({
            "aria-selected" : "true"
        });
        $("#myuw-event-filter-all").addClass("myuw-selected-button");
        $("#myuw-event-filter-breaks").attr({
            "aria-selected" : "false"
        });
        $("#acal-events-wrapper").attr("aria-labelledby", "myuw-events-filter-all");
        $(".acal-page-event").show();
    },
    filter_breaks: function() {
        $(".myuw-selected-button").removeClass("myuw-selected-button");
        $("#myuw-event-filter-all").attr({
            "aria-selected" : "false"
        });
        $("#myuw-event-filter-breaks").addClass("myuw-selected-button");
        $("#myuw-event-filter-breaks").attr({
            "aria-selected" : "true"
        });
        $("#acal-events-wrapper").attr("aria-labelledby", "myuw-events-filter-breaks");

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
        $("#myuw-event-filter-all").click(AcademicCalendarCard.filter_all);
        $("#myuw-event-filter-breaks").click(AcademicCalendarCard.filter_breaks);
        $("#myuw-event-filter-classes").click(AcademicCalendarCard.filter_classes);
    }
};
