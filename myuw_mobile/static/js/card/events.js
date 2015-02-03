var EventsCard = {
    name: 'EventsCard',
    dom_target: undefined,

    render_init: function() {
        //WSData.fetch_events_for_user(EventsCard.render_upon_data, EventsCard.show_error);
        console.log('woo');
        EventsCard._render()
    },

    render_upon_data: function() {
        if (!EventsCard._has_all_data()) {
            return;
        }
        EventsCard._render(WSData.event_data());
    },

    _render: function () {
        var source = $("#events_card_content").html();
        var template = Handlebars.compile(source);

        EventsCard.dom_target.html(template({display_card: true}));
        EventsCard.add_events();
    },

    _has_all_data: function () {
        return true;
        //if (WSData.event_data()) {
        //    return true;
        //}
        //return false;
    },

    add_events: function() {
        console.log('wasd');
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
