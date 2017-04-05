var AccountsCard = {
    name: 'AccountsCard',
    dom_target: undefined,

    render_init: function() {
        AccountsCard._render();
    },

    _render: function() {
        var source   = $("#accounts_card").html();
        var template = Handlebars.compile(source);
        var compiled = template({"card_name": AccountsCard.name});
        AccountsCard.dom_target.html(compiled);
    }
};
