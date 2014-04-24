var RegStatusCard = {
    render: function (notice_data) {
        var notices = [];
        if (notice_data.Registration !== undefined) {
            notices = notice_data.Registration.notices;
        }

        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        return template({ 
            reg_notices: notices 
        });
    }
};
