var NoticeBanner = {
    dom_target: undefined,

    render_init: function(dom_taget) {
        NoticeBanner.dom_target  = dom_taget;
        WSData.fetch_notice_data(NoticeBanner.render);
    },

    render: function () {
        var notice_data = WSData.notice_data();

        if (notice_data.length > 0) {
            var source = $("#notice_banner").html();
            var template = Handlebars.compile(source);
            var notices = Notices.get_categorized_critical_notices();
            var sorted_notices = NoticeBanner._sort_categories(notices);

            var html = template({
                "total_unread": Notices.get_total_unread(),
                "categorized_critical": sorted_notices
            });
            NoticeBanner.dom_target.html(html);
        }
    },

    _sort_categories: function (notices) {
        var category_order = ['Holds',
        'Fees & Finances',
        'Graduation',
        'Academics',
        'Registration',
        'Insurance',
        'Legal',
        'Visa'];
        var sorted_notices = [];
        $.each(category_order, function(idx, category){
            if (category in notices) {
                sorted_notices.push(notices[category]);
            }

        });
        return sorted_notices;


    }
};

