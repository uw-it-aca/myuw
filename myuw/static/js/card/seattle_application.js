var SeattleApplicationCard = {
    name: 'SeattleApplicationCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.applicant) {
            WSData.fetch_applicant_data(SeattleApplicationCard.render_upon_data, SeattleApplicationCard.render_error);
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
        var applicant_info = WSData.applicant_data();
        var seattle_application;
        for(var i = 0; i < applicant_info.length; i++){
            if(applicant_info[i].is_seattle) {
                seattle_application = applicant_info[i];
            }
        }

        if (typeof seattle_application === 'undefined' ||
            seattle_application.no_ug_app) {
            this.render_error();
            return;
        }

        var source = $("#seattle_application_card").html();
        var template = Handlebars.compile(source);

        SeattleApplicationCard.dom_target.html(template(seattle_application));
        LogUtils.cardLoaded(SeattleApplicationCard.name, SeattleApplicationCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.applicant_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#SeattleApplicationCard").hide();
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.SeattleApplicationCard = SeattleApplicationCard;
