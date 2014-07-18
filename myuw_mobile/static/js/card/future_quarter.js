var FutureQuarterCard = {
    name: 'FutureQuarterCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_oquarter_data(FutureQuarterCard.render_upon_data);
    },

    render_upon_data: function() {
        if (!FutureQuarterCard._has_all_data()) {
            FutureQuarterCard.dom_target.html(CardWithError.render());
            return;
        }
        FutureQuarterCard._render(WSData.oquarter_data());
    },

    _render: function (oquarter_data) {
        var source = $("#future_quarter_card").html();
        var template = Handlebars.compile(source);
        FutureQuarterCard.dom_target.html(template(oquarter_data));
    },

    _has_all_data: function () {
        if (WSData.oquarter_data()) {
            return true;
        }
        return false;
    }

};
