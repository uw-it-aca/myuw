var RegStatusCard = {
    render: function (notice_data) {
        var reg_notices = RegStatusCard._get_registration_notices(notice_data);
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        return template({"reg_notices": reg_notices});
    },

    _get_registration_notices: function (notice_data) {
        reg_notices = [];
        $.each(notice_data, function (group, notices) {
            if (group !== "total_unread"){
                notice_list = notices["notices"];
                $.each(notice_list, function (key, notice) {
                    if (notice.category === "Registration") {
                        reg_notices.push(notice);
                    }
                });
            }
        });
        return reg_notices;
    }
};
