var EventsCard = {
    name: 'EventsCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_event_data(EventsCard.render_upon_data, EventsCard.show_error);
    },

    render_upon_data: function() {
        if (!EventsCard._has_all_data()) {
            return;
        }
        EventsCard._render(WSData.dept_event_data());
    },

    _render: function () {
        var source = $("#events_card_content").html();
        var template = Handlebars.compile(source);
        var event_data = WSData.dept_event_data();
        var active_events = 0;
        var active_name_url = [];
        for (var key in event_data.active_cals){
            if (event_data.active_cals.hasOwnProperty(key)){
                active_events += event_data.active_cals[key].count;
                active_name_url.push({title: event_data.active_cals[key].title,
                                      url: event_data.active_cals[key].base_url});
            }
        }
        if (event_data.events.length === 0 && active_events === 0){
            EventsCard.dom_target.html('');
            return;
        }

        $.each(event_data.events, function(i, event){
            event.start = EventsCard.fix_event_time(event.start);
            event.start_time = moment(event.start).format('h:mm A');
        });

        var grouped_events = EventsCard.group_by_date(event_data.events);
        //determine if disclosure is required
        var needs_disclosure = (grouped_events[0].length > 0);

        EventsCard.dom_target.html(template({display_card: true,
                                             grouped_events_display: grouped_events[0],
                                             grouped_events_hide: grouped_events[1],
                                             has_events: event_data.events.length > 0,
                                             needs_disclosure: needs_disclosure,
                                             multi_active: active_name_url.length > 1,
                                             active_events: active_events,
                                             active_name_url: active_name_url,
                                             active_count: active_name_url.length
                                        }));
        EventsCard.add_events();
    },

    _has_all_data: function () {
        if (WSData.dept_event_data()) {
            return true;
        }
        return false;
    },


    group_by_date: function (event_data) {
        // assumes events are sorted server side
        var hide_events = [],
            show_events = [],
            last_date_show = null,
            last_date_hide = null,
            idx = 0,
            i = 0;

        for (i = 0; i < event_data.length; i++){
            var event = event_data[i];
            //Split off time range that brakes parsing
            var date = event.start.split(" ")[0];

            var day = moment(date).calendar();
            var formatted_date = null;
            if (i < 6) {
                if (day !== last_date_show) {
                    // Don't increment day index on first event
                    if (i > 0){
                        idx += 1;
                    }

                    last_date_show = day;
                    formatted_date = moment(date).format("dddd, MMMM D");
                    show_events[idx] = {'date_string': formatted_date,
                                            'events': []};

                }
                show_events[idx].events.push(event);
            } else {
                if (day !== last_date_hide) {
                    // Don't increment day index on first event
                    if (i > 0){
                        idx += 1;
                    }

                    last_date_hide = day;
                    formatted_date = moment(date).format("dddd, MMMM D");
                    hide_events[idx] = {'date_string': formatted_date,
                                            'events': []};

                }
                hide_events[idx].events.push(event);
            }
        }
        return [show_events, hide_events];
    },

    fix_event_time: function (timestamp) {
        // Will return the time, regardless if timestamp includes a range
        var date = timestamp.split(" ")[0];
        var time = timestamp.split(" ")[1];
        if (time === undefined){{
            return date;
        }}
        if (time.indexOf("-") > -1){
            time = time.substring(0, time.indexOf('-'));
        }
        return date + " " + time;
    },

    add_events: function() {
        $("#toggle_event_card_resources").on("click", function(ev) {
            ev.preventDefault();
            $("#events_card_more").toggleClass("slide-show");
            var card = $(ev.target).closest("[data-type='card']");

            if ($("#events_card_more").hasClass("slide-show")) {
                $("#toggle_event_card_resources").text("SHOW LESS");
                $("#toggle_event_card_resources").attr("title", "Hide additional academic resources");
                $("#events_card_more").attr("aria-hidden", "false");
                window.myuw_log.log_card(card, "expand");
            }
            else {
                $("#toggle_event_card_resources").text("SHOW MORE");
                $("#toggle_event_card_resources").attr("title", "Expand to show additional academic resources");
                $("#events_card_more").attr("aria-hidden", "true");
                window.myuw_log.log_card(card, "collapse");

                setTimeout(function() {
                    $("#toggle_event_card_resources").text("SHOW MORE");
                }, 700);
            }
        });
    },

    show_error: function() {
    }

    
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.EventsCard = EventsCard;