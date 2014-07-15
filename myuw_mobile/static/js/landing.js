var Landing = {
    render: function() {
        showLoading();
        Landing.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var landing_source = $("#landing").html();
        var template = Handlebars.compile(landing_source);
         $("#main-content").html(template());

        WSData.fetch_notice_data(Landing.render_notice_banner);

        var cards = [RegStatusCard,
                     VisualScheduleCard,
                     CourseCard,
                     FutureQuarterCard,
                     TuitionCard,
                     PCETuitionCard,
                     TextbookCard,
                     HfsCard,
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
