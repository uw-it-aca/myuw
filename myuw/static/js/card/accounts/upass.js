var UPassCard = {
    name: 'UPassCard',
    dom_target: undefined,

    render_init: function () {
        WSData.fetch_upass_data(UPassCard.render_upon_data, UPassCard.render_error);
    },

    render_error: function (status) {
        if (status === 543) {
            UPassCard._render_with_context({has_error: true});
            return;
        }
        remove_card(UPassCard.dom_target);
    },

    render_upon_data: function () {
        UPassCard._render();
    },
    _render_with_context: function(context){
        var source = $("#upass_card").html();
        var template = Handlebars.compile(source);
        var raw = template(context);
        UPassCard.dom_target.html(raw);
    },

    _render: function () {
        var template_data = WSData.upass_data();
        template_data.is_tacoma_student = window.user.tacoma;
        template_data.is_bothell_student = window.user.bothell;
        template_data.is_seattle_student = window.user.seattle;
        template_data.is_pce_student = window.user.pce;
        template_data.is_pce_or_seattle_student = template_data.is_seattle_student || template_data.is_pce_student;
        UPassCard._render_with_context(template_data);
        LogUtils.cardLoaded(UPassCard.name, UPassCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.UPassCard = UPassCard;
