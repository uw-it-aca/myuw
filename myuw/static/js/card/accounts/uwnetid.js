var UwnetidCard = {
    name: 'UwnetidCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_profile_data(UwnetidCard.render, UwnetidCard.render_error);
    },

    render_error: function() {
        UwnetidCard._render_with_context({has_error: true})
    },

    _render_with_context: function(context){
        var source   = $("#uwnetid_accounts_card").html();
        var template = Handlebars.compile(source);
        var compiled = template(context);
        UwnetidCard.dom_target.html(compiled);
    },

    render: function() {
        var data = WSData.profile_data().password;
        data.display_2fa = window.user.pmt_2fa;
        UwnetidCard._render_with_context(data);
        LogUtils.cardLoaded(UwnetidCard.name, UwnetidCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.UwnetidCard = UwnetidCard;
