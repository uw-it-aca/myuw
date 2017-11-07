var TacomaApplicationCard = {
    name: 'TacomaApplicationCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.applicant && !window.user.student) {
            WSData.fetch_profile_data(TacomaApplicationCard.render_upon_data, TacomaApplicationCard.render_error);
        } else {
            $("#TacomaApplicationCard").hide();
            return;
        }
    },

    render_upon_data: function () {
        if (!TacomaApplicationCard._has_all_data()) {
            return;
        }
        TacomaApplicationCard._render();
    },

    _render: function () {
        var applicant_info = WSData.profile_data();
        var source = $("#tacoma_application_card").html();
        var template = Handlebars.compile(source);

        TacomaApplicationCard.dom_target.html(template(applicant_info));
        LogUtils.cardLoaded(TacomaApplicationCard.name, TacomaApplicationCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.profile_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#TacomaApplicationCard").hide();
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.TacomaApplicationCard = TacomaApplicationCard;
