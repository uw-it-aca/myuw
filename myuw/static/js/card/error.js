var CardWithError = {
    render: function(card_name) {
        var source   = $("#card_with_error").html();
        var template = Handlebars.compile(source);
        return template({"card_name": card_name});
    },
};
