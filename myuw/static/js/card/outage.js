var OutageCard = {
    name: 'OutageCard',
    dom_target: undefined,

    render_init: function() {
        OutageCard._render();
    },

    _render: function () {
        var source = $("#outage_card_content").html();
        var template = Handlebars.compile(source);

        OutageCard.dom_target.html(template());
        LogUtils.cardLoaded(OutageCard.name, OutageCard.dom_target);
    }
};
