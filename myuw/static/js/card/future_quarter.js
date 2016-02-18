var FutureQuarterCard = {
    name: 'FutureQuarterCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.student) {
            $("#FutureQuarterCardA").hide();
            $("#FutureQuarterCard1").hide();
        }
        WSData.fetch_oquarter_data(FutureQuarterCard.render_upon_data, FutureQuarterCard.render_error);
    },

    render_upon_data: function() {
        if (!FutureQuarterCard._has_all_data()) {
            return;
        }

        if (WSData.oquarter_data().highlight_future_quarters) {
            FutureQuarterCard.dom_target = $('#FutureQuarterCardA');
            $("#FutureQuarterCard1").hide();
        }
        else {
            FutureQuarterCard.dom_target = $('#FutureQuarterCard1');
            $("#FutureQuarterCardA").hide();
        }

        FutureQuarterCard._render(WSData.oquarter_data());
    },

    _render: function (oquarter_data) {
        var source = $("#future_quarter_card").html();
        var template = Handlebars.compile(source);

        if (!oquarter_data.terms.length) {
            FutureQuarterCard.dom_target.hide();
        }
        else {
            FutureQuarterCard.dom_target.html(template(oquarter_data));
            LogUtils.cardLoaded(FutureQuarterCard.name, FutureQuarterCard.dom_target);
        }
    },

    render_error: function() {
        FutureQuarterCard.dom_target.html(CardWithError.render());
    },

    _has_all_data: function () {
        if (WSData.oquarter_data()) {
            return true;
        }
        return false;
    }

};


// One of these 2 needs to actually call render_init - A for arbitrary.
var FutureQuarterCardA = {
    name: 'FutureQuarterCardA',
    render_init: function() { FutureQuarterCard.render_init(); }
};

var FutureQuarterCard1 = {
    name: 'FutureQuarterCard1',
    render_init: function() {}
};

