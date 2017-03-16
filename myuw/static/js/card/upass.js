var UPassCard = {
    name: 'UPassCard',
    dom_target: undefined,

    render_init: function () {
        TextbookCard.dom_target = $('#UPassCard');
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
        template_data.is_tacoma_student = window.user.tacoma_affil;
        template_data.is_bothell_student = window.user.bothell_affil;
        template_data.is_seattle_student = window.user.seattle_affil;
        template_data.is_pce_student = window.user.pce;

        var source = $("#upass_card").html();
        var template = Handlebars.compile(source);
        var raw = template(template_data);
        UPassCard.dom_target.html(raw);
        LogUtils.cardLoaded(UPassCard.name, UPassCard.dom_target);
    },
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.UPassCard = UPassCard;
