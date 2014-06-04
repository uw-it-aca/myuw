var NoticeBanner = {
    render: function (notice_data) {
        var unread_categories = Notices.get_unread_count_by_category();
        var source = $("#notice_banner").html();
        var template = Handlebars.compile(source);

        return template({
            "total_unread": Notices.get_total_unread(),
            "week_critical": Notices.get_critical_this_week()
        });
    }
};

