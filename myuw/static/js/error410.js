var Error410 = {

    render: function() {
        var source = $("#future_410_error").html();
        var template = Handlebars.compile(source);
        var raw = template({});
        $("#main-content").html(raw);
    }
};
