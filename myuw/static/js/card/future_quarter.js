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
        var source = $("#future_quarter_card").html();
        var template = Handlebars.compile(source);

        if (!oquarter_data.terms.length) {
            FutureQuarterCard.dom_target.hide();
            return;
        }
        var raw = template(oquarter_data);
        FutureQuarterCard.dom_target.html(raw);
        LogUtils.cardLoaded(FutureQuarterCard.name, FutureQuarterCard.dom_target);
    },

    render_error: function(status) {
        $("#FutureQuarterCard1").hide();
        if (status === 404) {
            FutureQuarterCard.dom_target.hide();
            return;
        }
        $("#FutureQuarterCardA").html(CardWithError.render("Future Quarter Courses"));
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
