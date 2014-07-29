var UwEmail = {

    render_init: function() {
        WSData.fetch_uwemail_data(UwEmail.render_upon_data);
    },

    render_upon_data: function() {
        var source = $("#uwemail-content").html();
        var template = Handlebars.compile(source);
        $("#uwemail").html(template(WSData.uwemail_data()));
    }
};
