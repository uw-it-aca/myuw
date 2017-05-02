var MedicineAccountsCard = {
    name: 'Medicine--AccountsCard',
    dom_target: undefined,

    render_init: function() {
        MedicineAccountsCard._render();
    },

    _render: function() {
        var source   = $("#accounts_medicine").html();
        var template = Handlebars.compile(source);
        var compiled = template({"card_name": MedicineAccountsCard.name});
        MedicineAccountsCard.dom_target.html(compiled);
    }
};
