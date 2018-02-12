var AlumniCard = {
    name: 'AlumniCard',
    dom_target: undefined,

    render_init: function() {
        AlumniCard._render();
    },

    _render: function () {
        var source = $("#alumni_card_content").html();
        var template = Handlebars.compile(source);
        var alumni_data = {
            "alum_asso": window.user.alum_asso
            };
        AlumniCard.dom_target.html(template(alumni_data));
        LogUtils.cardLoaded(AlumniCard.name, AlumniCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.AlumniCard = AlumniCard;
