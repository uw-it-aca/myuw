var Notices = {
    show_notices: function() {
        source = $("#notices").html();
        template = Handlebars.compile(source);

        $("#courselist").html(template());
    }
};
