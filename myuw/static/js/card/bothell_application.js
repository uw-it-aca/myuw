var BothellApplicationCard = {
    name: 'BothellApplicationCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.applicant) {
            WSData.fetch_applicant_data(BothellApplicationCard.render_upon_data, BothellApplicationCard.render_error);
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
        var applicant_info = WSData.applicant_data();

        var bothell_application;
        for(var i = 0; i < applicant_info.length; i++){
            if(applicant_info[i].is_bothell) {
                bothell_application = applicant_info[i];
            }
        }

        if (typeof bothell_application === 'undefined' ||
            bothell_application.no_ug_app){
            this.render_error();
            return;
        }

        var source = $("#bothell_application_card").html();
        var template = Handlebars.compile(source);

        BothellApplicationCard.dom_target.html(template(bothell_application));
        LogUtils.cardLoaded(BothellApplicationCard.name, BothellApplicationCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.applicant_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#BothellApplicationCard").hide();
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.BothellApplicationCard = BothellApplicationCard;
