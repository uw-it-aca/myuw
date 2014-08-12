var FutureQuarter = {
    render: function(term) {
        Navbar.render_navbar();
        UwEmail.render_init();
        showLoading();
        FutureQuarter.make_html(term);
    },

    make_html: function (term) {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var page_source = $("#future").html();
        var template = Handlebars.compile(page_source);
        $("#main-content").html(template({"term": term}));

        WSData.fetch_notice_data(Landing.render_notice_banner);

        var cards = [VisualScheduleCard,
                     CourseCard,
                     TextbookCard];

        Cards.load_cards_in_order(cards, $("#future_content"), term);
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
