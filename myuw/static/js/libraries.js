var Libraries = {
    show_card: function() {
        source = $("#libraries").html();
        template = Handlebars.compile(source);

        $("#main-content").html(template());
    }
};
