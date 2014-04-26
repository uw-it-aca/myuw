var Landing = {
    render: function() {
        showLoading();
        WSData.fetch_notice_data(Landing.make_html);
    },

    make_html: function() {
        var notice_data = WSData.notice_data();
        var source = $('#landing').html();
        var template = Handlebars.compile(source);

        var notice_banner = '';
        if (notice_data.total_unread > 0) {
            notice_banner = NoticeBanner.render(notice_data);
        }

        reg_notices = filter_notices_by_category('Registration', notice_data);
        var reg_status_card = ''
        if (reg_notices.length > 0) {
            reg_status_card = RegStatusCard.render(reg_notices);
        }

        $('#courselist').html(template({
            notice_banner: notice_banner,
            reg_status_card: reg_status_card
        }));

    }
};
