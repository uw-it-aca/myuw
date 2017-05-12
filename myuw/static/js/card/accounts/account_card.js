var AccountsCard = {
    name: 'AccountsCard',
    dom_target: undefined,

    render_init: function() {
        AccountsCard._render();
    },

    _render: function() {
        var source   = $("#accounts_card").html();
        var template = Handlebars.compile(source);
        var compiled = template({
            card_name: AccountsCard.name,
            is_faculty: window.user.faculty,
            is_clinician: window.user.clinician
        });
        AccountsCard.dom_target.html(compiled);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.AccountsCard = AccountsCard;
