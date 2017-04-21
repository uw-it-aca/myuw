var EventsCard = {
    name: 'EventsCard',
    dom_target: undefined,

    render_init: function() {
        WebServiceData.require({event_data: new EventData()}, EventsCard.render);
    },

    render: function (resources) {
        var source = $("#events_card_content").html();
        var template = Handlebars.compile(source);
        var active_events = 0;
        var active_name_url = [];
        var event_data_resource = resources.event_data;

        if (EventsCard.show_error(event_data_resource.error)) {
            return;
        }

        var event_data = event_data_resource.data;
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
            var start_date = moment(new Date(event.start)).tz('America/Los_Angeles');
            var end_date = moment(new Date(event.end)).tz('America/Los_Angeles');
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
        LogUtils.cardLoaded(EventsCard.name, EventsCard.dom_target);
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
        $(".toggle_event_card_resources").on("click", function(ev) {
            ev.preventDefault();
            var card = $(ev.target).closest("[data-type='card']");
            var div = $("#events_card_more");
            var expose = $("#show_event_resources_wrapper");
            var hide = $("#hide_event_resources_wrapper");
            toggle_card_disclosure(card, div, expose, hide, "");
        });
    },

    show_error: function(event_data_error) {
        if (event_data_error) {
            EventsCard.dom_target.hide();
            return true;
        }

        return false;
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.EventsCard = EventsCard;
