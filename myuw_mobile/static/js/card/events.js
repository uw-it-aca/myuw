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
            console.log(event_data.active_cals[key]);
            if (event_data.active_cals.hasOwnProperty(key)){
                active_events += event_data.active_cals[key].count
                active_name_url.push({title: event_data.active_cals[key].title,
                                      url: event_data.active_cals[key].base_url});
            }
        }
        if (event_data.events.length === 0 && active_events === 0){
            EventsCard.dom_target.html('');
            return;
        }

        EventsCard.dom_target.html(template({display_card: true,
                                             data: event_data,
                                             has_events: event_data.events.length > 0,
                                             needs_disclosure: false,
                                             multi_active: active_name_url.length > 1,
                                             active_events: active_events,
                                             active_name_url: active_name_url,
                                             active_count: active_name_url.length
                                        }));
        EventsCard.add_events();
    },

    _has_all_data: function () {
        return true;
        if (WSData.dept_event_data()) {
            return true;
        }
        return false;
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
