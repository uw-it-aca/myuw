var SeattleApplicationCard = {
    name: 'SeattleApplicationCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.applicant && !window.user.student) {
            WSData.fetch_profile_data(SeattleApplicationCard.render_upon_data, SeattleApplicationCard.render_error);
        } else {
            $("#SeattleApplicationCard").hide();
            return;
        }
    },

    render_upon_data: function () {
        if (!SeattleApplicationCard._has_all_data()) {
            return;
        }
        SeattleApplicationCard._render();
    },

    _render: function () {
        var applicant_info = WSData.profile_data();
        var source = $("#seattle_application_card").html();
        var template = Handlebars.compile(source);

        SeattleApplicationCard.dom_target.html(template(applicant_info));
        LogUtils.cardLoaded(SeattleApplicationCard.name, SeattleApplicationCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.profile_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#SeattleApplicationCard").hide();
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.SeattleApplicationCard = SeattleApplicationCard;
