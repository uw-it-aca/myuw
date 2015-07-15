var NoticeBanner = {
    dom_target: undefined,

    render_init: function(dom_taget) {
        NoticeBanner.dom_target  = dom_taget;
        WSData.fetch_notice_data(NoticeBanner.render);
    },

    render: function () {
        var notice_data = WSData.notice_data();
        Notices.get_categorized_critical_notices();

        if (notice_data.length > 0) {
            var source = $("#notice_banner").html();
            var template = Handlebars.compile(source);

            var html = template({
                "total_unread": Notices.get_total_unread(),
                "categorized_critical":
                    Notices.get_categorized_critical_notices()
            });
            NoticeBanner.dom_target.html(html);
        }
    }
};

