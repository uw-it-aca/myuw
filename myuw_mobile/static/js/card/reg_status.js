var RegStatusCard = {
    render: function (reg_notices) {
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        return template({"reg_notices": reg_notices});
    },

};
