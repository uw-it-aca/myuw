var MessageBanner = {
    dom_target: undefined,

    render_init: function(dom_taget) {
        MessageBanner.dom_target  = dom_taget;
        WSData.fetch_message_data(MessageBanner.render);
    },

    render: function () {
        var message_data = WSData.message_data();

        if (message_data.length > 0) {
            var source = $("#message_banner").html();
            var template = Handlebars.compile(source);

            var html = template({
                "messages": message_data
            });
            MessageBanner.dom_target.html(html);

        } else {
            MessageBanner.dom_target.hide();
        }
    },

};
