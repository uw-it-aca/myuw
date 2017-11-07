var WelcomeCard = {
    name: 'WelcomeCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.applicant && !window.user.student) {
            this._render()
        } else {
            return;
        }
    },

    render_upon_data: function () {
        WelcomeCard._render();
    },

    _render: function () {
        var student_info = {};
        var source = $("#welcome_card").html();
        var template = Handlebars.compile(source);

        WelcomeCard.dom_target.html(template(student_info));
        LogUtils.cardLoaded(WelcomeCard.name, WelcomeCard.dom_target);
    },

    _has_all_data: function () {
        return true;
    },

    render_error: function () {
        $("#WelcomeCard").hide();
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.WelcomeCard = WelcomeCard;
