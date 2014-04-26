var NoticeBanner = {
    render: function (notice_data) {
        var unread_categories = NoticeBanner._get_categories(notice_data);
        var source = $("#notice_banner").html();
        var template = Handlebars.compile(source);
        return template({
            "total_unread": notice_data.total_unread,
            "categories": unread_categories.sort()
        });
    },
    _get_categories: function (notice_data) {
        categories = [];
        $.each(notice_data, function (group, notices) {
            if (group !== "total_unread"){
                notice_list = notices["notices"];
                $.each(notice_list, function (key, notice) {
                    if (!notice.is_read &&  
                        $.inArray(notice.category, categories) == -1) {
                        categories.push(notice.category);
                    }
                });
            }
        });
        return categories;
    }
};

