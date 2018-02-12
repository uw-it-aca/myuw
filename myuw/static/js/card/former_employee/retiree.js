var RetireAssoCard = {
    name: 'RetireAssoCard',
    dom_target: undefined,

    render_init: function() {
        RetireAssoCard._render();
    },

    _render: function () {
        var source = $("#retire_asso_card_content").html();
        var template = Handlebars.compile(source);
        RetireAssoCard.dom_target.html(template({}));
        LogUtils.cardLoaded(RetireAssoCard.name, RetireAssoCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.RetireAssoCard = RetireAssoCard;
