var UPassCard = {
    name: 'UPassCard',
    dom_target: undefined,

    render_init: function () {
        WSData.fetch_upass_data(UPassCard.render_upon_data,
                                UPassCard.render_error);
    },

    render_error: function (status) {
        // notice never returns 404.
        if (status === 404) {
            // not student or SDB can't find the regid
            UPassCard.dom_target.hide();
            return;
        }
        var raw = CardWithError.render("Tuition & Fees");
        UPassCard.dom_target.html(raw);
    },

    render_upon_data: function () {
        // _render should be called only once.
        if (renderedCardOnce(UPassCard.name)) {
            return;
        }
        UPassCard._render();
    },

    _render: function () {
        var template_data = WSData.upass_data();

        var source = $("#upass_card").html();
        var template = Handlebars.compile(source);
        UPassCard.dom_target.html(template(template_data));
        LogUtils.cardLoaded(UPassCard.name, UPassCard.dom_target);
    },
}

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.UPassCard = UPassCard;
