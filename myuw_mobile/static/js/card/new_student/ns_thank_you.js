var ThankYouCard = {
    name: 'ThankYouCard',
    dom_target: undefined,
    render_init: function() {
        ThankYouCard.dom_target.html(ThankYouCard.render());
    },

    render: function () {
        var source = $("#ns_thank_you").html();
        var template = Handlebars.compile(source);
        return template({});
    },
};
