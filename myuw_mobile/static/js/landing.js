var Landing = {
    render: function() {
        showLoading();
        WSData.fetch_notice_data(Landing.make_html);
        WSData.fetch_tuition_data(null);
        WSData.fetch_current_course_data(VisualScheduleCard.render_upon_data);
        WSData.fetch_hfs_data(HfsCard.render_upon_data);
        WSData.fetch_library_data(LibraryCard.render_upon_data);
    },

    make_html: function() {
        $('html,body').animate({scrollTop: 0}, 'fast');
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
        var fin_aid_card = '';
        if (fina_notices.notices.length > 0 || WSData.tuition_data()) {
            fin_aid_card = FinAidCard.render(fina_notices);
        }

        $('#main-content').html(template({
            notice_banner: notice_banner,
            reg_status_card: reg_status_card,
            tuition_card: tuition_card,
            pce_tuition_card: pce_tuition_card,
            fin_aid_card: fin_aid_card
        }));

        VisualScheduleCard.render_init();
        CourseCard.render_init();
        HfsCard.render_init();
        LibraryCard.render_init();
    },

};
