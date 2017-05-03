var AccountsCard = {
    name: 'AccountsCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_profile_data(AccountsCard._render);
    },

    _render: function() {
        var source   = $("#accounts_card").html();
        var template = Handlebars.compile(source);
        var compiled = template(WSData.profile_data().password);
        AccountsCard.dom_target.html(compiled);
    }
};
