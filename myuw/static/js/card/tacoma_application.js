var TacomaApplicationCard = {
    name: 'TacomaApplicationCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.applicant) {
            WSData.fetch_applicant_data(TacomaApplicationCard.render_upon_data, TacomaApplicationCard.render_error);
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
        var applicant_info = WSData.applicant_data();

        for(var i = 0; i < applicant_info.length; i++){
            if(applicant_info[i].is_tacoma) {
                tacoma_application = applicant_info[i];
            }
        }

        if (typeof tacoma_application === 'undefined' ||
            tacoma_application.no_ug_app){
            this.render_error();
            return;
        }

        var source = $("#tacoma_application_card").html();
        var template = Handlebars.compile(source);

        TacomaApplicationCard.dom_target.html(template(tacoma_application));
        LogUtils.cardLoaded(TacomaApplicationCard.name, TacomaApplicationCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.applicant_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#TacomaApplicationCard").hide();
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.TacomaApplicationCard = TacomaApplicationCard;
