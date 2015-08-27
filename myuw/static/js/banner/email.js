var UwEmail = {

    render_upon_data: function() {
        var source = $("#uwemail-content").html();
        var template = Handlebars.compile(source);
        $("#uwemail").html(template(WSData.uwemail_data()));
    }
};
