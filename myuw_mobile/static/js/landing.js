var Landing = {
    render: function() {
        Navbar.render_navbar();
        showLoading();
        UwEmail.render_init();
        Landing.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var landing_source = $("#landing").html();
        var template = Handlebars.compile(landing_source);
        
        $("#main-content").html(template());

        WSData.fetch_notice_data(Landing.render_notice_banner);

        var cards = [RegStatusCard,
                     FutureQuarterCard,
                     VisualScheduleCard,
                     CourseCard,
                     HfsCard,
                     TuitionCard,
                     LibraryCard];


        Cards.load_cards_in_order(cards, $("#landing_content"));


    },

    render_notice_banner: function () {
        var notice_banner = '',
            notice_data = WSData.notice_data();
        if (Notices.get_total_unread() > 0) {
            notice_banner = NoticeBanner.render(notice_data);
        }
        $("#notice_banner_location").html(notice_banner);
    }

};
