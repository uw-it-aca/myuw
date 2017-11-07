var BothellApplicationCard = {
    name: 'BothellApplicationCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.applicant && !window.user.student) {
            WSData.fetch_profile_data(BothellApplicationCard.render_upon_data, BothellApplicationCard.render_error);
        } else {
            $("#BothellApplicationCard").hide();
            return;
        }
    },

    render_upon_data: function () {
        if (!BothellApplicationCard._has_all_data()) {
            return;
        }
        BothellApplicationCard._render();
    },

    _render: function () {
        var applicant_info = WSData.profile_data();
        var source = $("#seattle_application_card").html();
        var template = Handlebars.compile(source);

        BothellApplicationCard.dom_target.html(template(applicant_info));
        LogUtils.cardLoaded(BothellApplicationCard.name, BothellApplicationCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.profile_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#BothellApplicationCard").hide();
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.BothellApplicationCard = BothellApplicationCard;
