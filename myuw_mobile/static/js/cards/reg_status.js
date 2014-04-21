var RegStatusCard = {
    render_card: function () {
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        return template();
    }
};
