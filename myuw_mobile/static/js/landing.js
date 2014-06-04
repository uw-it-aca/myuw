var Landing = {
    render: function() {
        showLoading();
        WSData.fetch_notice_data(Landing.make_html);
        WSData.fetch_tuition_data();
        WSData.fetch_library_data();
    },

    make_html: function() {
        var notice_data = WSData.notice_data();
        var source = $('#landing').html();
        var template = Handlebars.compile(source);

        var notice_banner = '';
        if (Notices.get_total_unread() > 0) {
            notice_banner = NoticeBanner.render(notice_data);
        }

        reg_notices = Notices.get_notices_for_category("Registration");
        var reg_status_card = ''
        if (reg_notices.notices.length > 0) {
            reg_status_card = RegStatusCard.render(reg_notices);
        }

        fina_notices = Notices.get_notices_for_category("Fees & Finances");
        var tuition_card = ''
        if (fina_notices.notices.length > 0 || WSData.tuition_data()) {
            tuition_card = TuitionCard.render(fina_notices);
        }

        var library_card = ''
        if (WSData.library_data()) {
            library_card = LibraryCard.render();
        }

        $('#main-content').html(template({
            notice_banner: notice_banner,
            reg_status_card: reg_status_card,
            tuition_card: tuition_card,
            library_card: library_card
        }));

    },


    // Filter non-holds notices by the given category
    // Return a list of notices
    filter_notices_by_category: function (category, notice_data) {
        reg_notices = notice_data.today.notices.concat(
            notice_data.week.notices, 
            notice_data.next_week.notices, 
            notice_data.future.notices);
        reg_notices = reg_notices.filter(function(notice) {
            if (notice.category === category) {
                return true;
            }
        });
        return reg_notices;
    }
};
