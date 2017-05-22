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

            MessageBanner.adjust_banner_padding();

            $(window).resize(function(){
                MessageBanner.adjust_banner_padding();
            });

        } else {
            MessageBanner.dom_target.hide();
        }
    },

    adjust_banner_padding: function () {

        var viewport_width = $(window).width();

        // set top padding based on height of message banner container
        // should be for tablet and desktop
        if (viewport_width > 1024) {
            var sHeight = $(".myuw-banner").prop('scrollHeight');
            $(".myuw-body .myuw-wrapper").css("padding-top", sHeight);
        }
        else {
            $(".myuw-body .myuw-wrapper").css("padding-top", "0px");
        }

    }
};
