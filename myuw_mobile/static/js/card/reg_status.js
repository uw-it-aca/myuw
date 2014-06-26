var RegStatusCard = {
    render: function (reg_notices) {
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        $('body').on('click', '#reg_show_resources', function () {
            console.log('click');
        });

        return template({"reg_notices": reg_notices});
    },
};

    
