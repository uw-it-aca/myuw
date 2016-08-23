var FutureQuarter = {
    render: function(term) {
        showLoading();
        CommonLoading.render_init();
        FutureQuarter.make_html(term);
    },

    make_html: function (term) {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var page_source = $("#future").html();
        var template = Handlebars.compile(page_source);
        $("#main-content").html(template({"term": term}));

        VisualScheduleCard.force_visual_schedule_display();
        NoticeBanner.render_init($("#notice_banner_location"));

        var cards = [VisualScheduleCard,
                     CourseCards,
                     TextbookCard];

        Cards.load_cards_in_order(cards, $("#future_content"), term);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.FutureQuarter = FutureQuarter;
