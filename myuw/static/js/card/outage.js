var OutageCard = {
    name: 'OutageCard',
    dom_target: undefined,

    render_init: function() {
        if(window.webservice_outage){
            OutageCard._render();
        } else {
            OutageCard.dom_target.hide();
        }
    },

    _render: function () {
        // In case previously hidden
        OutageCard.dom_target.show();

        var source = $("#outage_card_content").html();
        var template = Handlebars.compile(source);

        OutageCard.dom_target.html(template());
        LogUtils.cardLoaded(OutageCard.name, OutageCard.dom_target);
    }
};
