var Landing = {
    render: function() {
        showLoading();
        WSData.fetch_notice_data(Landing.make_html);
        WSData.fetch_tuition_data();
        WSData.fetch_hfs_data();
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

        var reg_notices = Notices.get_notices_for_category("Registration");
        var reg_status_card = '';
        if (reg_notices.notices.length > 0) {
            reg_status_card = RegStatusCard.render(reg_notices);
        }

        var tuition_card = '';
        var pce_tuition_card = '';
        if (WSData.tuition_data()){
            tuition_card = TuitionCard.render(WSData.tuition_data());
            pce_tuition_card = PCETuitionCard.render(WSData.tuition_data());
        }



        var fina_notices = Notices.get_notices_for_category("Fees & Finances");
        fin_aid_card = '';
        if (fina_notices.notices.length > 0 || WSData.tuition_data()) {
            fin_aid_card = FinAidCard.render(fina_notices);
        }

        var hfs_data = WSData.hfs_data();
        var hfs_card = '';
        if (hfs_data && (hfs_data.student_husky_card || hfs_data.employee_husky_card || hfs_data.resident_dining)) {
            hfs_card = HfsCard.render();
        }

        var library_card = '';
        if (WSData.library_data()) {
            library_card = LibraryCard.render();
        }

        $('#main-content').html(template({
            notice_banner: notice_banner,
            reg_status_card: reg_status_card,
            tuition_card: tuition_card,
            pce_tuition_card: pce_tuition_card,
            fin_aid_card: fin_aid_card,
            hfs_card: hfs_card,
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
