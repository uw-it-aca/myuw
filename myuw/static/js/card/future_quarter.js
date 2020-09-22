var FutureQuarterCard = {
    name: 'FutureQuarterCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.student) {
            $("#FutureQuarterCardA").hide();
            $("#FutureQuarterCard1").hide();
            return;
        }
        WSData.fetch_oquarter_data(FutureQuarterCard.render_upon_data, FutureQuarterCard.render_error);
    },

    render_upon_data: function() {
        if (!WSData.oquarter_data()) {
            return;
        }
        if (WSData.oquarter_data().highlight_future_quarters) {
            FutureQuarterCard.dom_target = $("#FutureQuarterCardA");
            $("#FutureQuarterCard1").hide();
        }
        else {
            FutureQuarterCard.dom_target = $('#FutureQuarterCard1');
            $("#FutureQuarterCardA").hide();
        }
        FutureQuarterCard._render(WSData.oquarter_data());
    },

    _render: function (oquarter_data) {
        if (!oquarter_data.terms.length) {
            FutureQuarterCard.dom_target.hide();
            return;
        }
        FutureQuarterCard._render_with_context(oquarter_data);
        LogUtils.cardLoaded(FutureQuarterCard.name, FutureQuarterCard.dom_target);
    },

    _render_with_context: function(context){
        var source = $("#future_quarter_card").html();
        var template = Handlebars.compile(source);
        var raw = template(context);
        FutureQuarterCard.dom_target.html(raw);
    },

    render_error: function(status) {
        if (status === 404) {
            // we don't know which card is showing
            if ($("#FutureQuarterCardA")) {
                $("#FutureQuarterCardA").hide();
            }
            if ($("#FutureQuarterCard1")) {
                $("#FutureQuarterCard1").hide();
            }
            return;
        }
        FutureQuarterCard._render_with_context({has_error: true});
    },
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


/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.FutureQuarterCard = FutureQuarterCard;
exports.FutureQuarterCardA = FutureQuarterCardA;
exports.FutureQuarterCard1 = FutureQuarterCard1;
