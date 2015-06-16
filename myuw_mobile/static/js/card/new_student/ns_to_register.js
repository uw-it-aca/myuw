var ToRegisterCard = {
    name: 'ToRegisterCard',
    dom_target: undefined,
    render_init: function() {
        ToRegisterCard.dom_target.html(ToRegisterCard.render());
    },

    render: function () {
        var source = $("#ns_to_register").html();
        var template = Handlebars.compile(source);
        return template({});
    },
};
