var Landing = {
    render: function() {
        showLoading();
        WSData.fetch_notice_data(Landing.make_html);
        WSData.fetch_tuition_data();
    },

    make_html: function() {
        var notice_data = WSData.notice_data();
        var source = $('#landing').html();
        var template = Handlebars.compile(source);

        var notice_banner = '';
        if (notice_data.total_unread > 0) {
            notice_banner = NoticeBanner.render(notice_data);
        }

        reg_notices = Landing.filter_notices_by_category('Registration', notice_data);
        var reg_status_card = ''
        if (reg_notices.length > 0) {
            reg_status_card = RegStatusCard.render(reg_notices);
        }

        fina_notices = Landing.filter_notices_by_category('Finance', notice_data);
        var tuition_card = ''
        if (fina_notices.length > 0) {
            tuition_card = TuitionCard.render(fina_notices);
        }

        $('#main-content').html(template({
            notice_banner: notice_banner,
            reg_status_card: reg_status_card,
            tuition_card: tuition_card
        }));

    },


    // Filter non-holds notices by the given category
    // Return a list of notices
    filter_notices_by_category: function (category, notice_data) {
        reg_notices = notice_data.today.notices.concat(
            notice_data.week.notices, 
            notice_data.future.notices);
        reg_notices = reg_notices.filter(function(notice) {
            if (notice.category === category) {
                return true;
            }
        });
        return reg_notices;
    }
};
