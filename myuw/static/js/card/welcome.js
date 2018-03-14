var WelcomeCard = {
    name: 'WelcomeCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.applicant && !window.user.student) {
            WSData.fetch_applicant_data(WelcomeCard.render_upon_data(), WelcomeCard.render_error());
        } else {
            console.log('hide at init');
            this.render_error();
        }
    },

    render_upon_data: function () {
        WelcomeCard._render();
    },

    _render: function () {
        var applicant_info = WSData.applicant_data();
        console.log(applicant_info);
        if(applicant_info){
            console.log('has app info');
            if(applicant_info.length === 0) {
                console.log("app len 0");
                WelcomeCard.render_error();
            }
        } else {
            var student_info = {};
            var source = $("#welcome_card").html();
            var template = Handlebars.compile(source);

            WelcomeCard.dom_target.html(template(student_info));
            LogUtils.cardLoaded(WelcomeCard.name, WelcomeCard.dom_target);
        }
    },

    _has_all_data: function () {
        return true;
    },

    render_error: function () {
        $("#WelcomeCard").hide();
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.WelcomeCard = WelcomeCard;
