var ApplicantProfileCard = {
    name: 'ApplicantProfileCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.applicant && !window.user.student) {
            WSData.fetch_profile_data(ApplicantProfileCard.render_upon_data, ApplicantProfileCard.render_error);
        } else {
            $("#ApplicantProfileCard").hide();
            return;
        }
    },

    render_upon_data: function () {
        if (!ApplicantProfileCard._has_all_data()) {
            return;
        }
        ApplicantProfileCard._render();
    },

    _render: function () {
        var student_info = WSData.profile_data();
        var source = $("#applicant_profile_card").html();
        var template = Handlebars.compile(source);

        ApplicantProfileCard.dom_target.html(template(student_info));
        LogUtils.cardLoaded(ApplicantProfileCard.name, ApplicantProfileCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.profile_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#ApplicantProfileCard").hide();
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.ApplicantProfileCard = ApplicantProfileCard;
