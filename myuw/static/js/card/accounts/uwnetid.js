var UwnetidCard = {
    name: 'UwnetidCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_profile_data(UwnetidCard.render, UwnetidCard.render_error);
    },

    render_error: function() {
        UwnetidCard.dom_target.html(CardWithError.render("UW NetID"));
    },

    render: function() {
        var data = WSData.profile_data().password;
        data.display_2fa = (window.user.stud_employee ||
                            window.user.employee ||
                            window.user.clinician);
        var source   = $("#accounts_card").html();
        var template = Handlebars.compile(source);
        var compiled = template(data);
        UwnetidCard.dom_target.html(compiled);
        LogUtils.cardLoaded(UwnetidCard.name, UwnetidCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.UwnetidCard = UwnetidCard;
