var Libraries = {
    show_card: function() {
        source = $("#libraries").html();
        console.log(source);
        template = Handlebars.compile(source);

        $("#courselist").html(template());
    }
};
