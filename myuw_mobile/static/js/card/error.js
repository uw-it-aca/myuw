var CardWithError = {
    render: function() {
        var source   = $("#card_with_error").html();
        var template = Handlebars.compile(source);
        return template({});
    },
};
