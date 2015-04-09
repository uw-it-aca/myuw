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
        for (var key in event_data.future_active_cals){
            if (event_data.future_active_cals.hasOwnProperty(key)){
                active_events += event_data.future_active_cals[key].count;
                active_name_url.push({title: event_data.future_active_cals[key].title,
                                      url: event_data.future_active_cals[key].base_url});
            }
        }
        if (event_data.events.length === 0 && active_events === 0){
            EventsCard.dom_target.html('');
            return;
        }

        $.each(event_data.events, function(i, event){
            var start_date = moment(event.start).tz('America/Los_Angeles');
            var end_date = moment(event.end).tz('America/Los_Angeles');
            event.start_time = start_date.format('h:mm A');
            event.start_date = start_date.format('YYYY-MM-DD');
            event.end_date = end_date.format('YYYY-MM-DD');
        });

        var grouped_events = EventsCard.group_by_date(event_data.events);
        //determine if disclosure is required
        var needs_disclosure = (grouped_events[1].length > 0);

        //determine if more than one active cals
        var multi_cal = (Object.keys(event_data.active_cals).length > 1);
        var cal_links = [];
        for (var key2 in event_data.active_cals) {
            if (event_data.active_cals.hasOwnProperty(key2)){
                cal_links.push(event_data.active_cals[key2]);
            }
        }

        EventsCard.dom_target.html(template({display_card: true,
                                             grouped_events_display: grouped_events[0],
                                             grouped_events_hide: grouped_events[1],
                                             hidden_event_count: grouped_events[1].length,
                                             has_events: event_data.events.length > 0,
                                             needs_disclosure: needs_disclosure,
                                             multi_active: active_name_url.length > 1,
                                             active_events: active_events,
                                             active_name_url: active_name_url,
                                             active_count: active_name_url.length,
                                             multi_cal: multi_cal,
                                             cal_links: cal_links
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
            idx = 0,
            i = 0;

        for (i = 0; i < event_data.length; i++){
            var event = event_data[i];

            if (i < 6) {
                show_events.push(event);
            } else {
                hide_events.push(event);
            }
        }
        return [show_events, hide_events];
    },

    add_events: function() {
        $("#toggle_event_card_resources").on("click", function(ev) {
            ev.preventDefault();
            $("#events_card_more").toggleClass("slide-show");
            var card = $(ev.target).closest("[data-type='card']");

            if ($("#events_card_more").hasClass("slide-show")) {
                window.user.event_toggle_text = $("#toggle_event_card_resources").text();
                $("#toggle_event_card_resources").text("SHOW LESS");
                $("#toggle_event_card_resources").attr("title", "Hide additional academic resources");
                $("#events_card_more").attr("aria-hidden", "false");
                window.myuw_log.log_card(card, "expand");
            }
            else {
                if (window.user.event_toggle_text === undefined) {
                    $("#toggle_event_card_resources").text("SHOW MORE");
                } else {
                    $("#toggle_event_card_resources").text(window.user.event_toggle_text);
                }

                $("#toggle_event_card_resources").attr("title", "Expand to show additional academic resources");
                $("#events_card_more").attr("aria-hidden", "true");
                window.myuw_log.log_card(card, "collapse");
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
