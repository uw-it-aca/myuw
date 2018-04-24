var Academics = {
    is_desktop: undefined,

    render: function() {
        showLoading();
        Academics.make_html();
    },

    make_html: function () {

        $('html,body').animate({scrollTop: 0}, 'fast');
        var source = $("#academics_page").html();
        var template = Handlebars.compile(source);
        $("#main-content").html(template());

        // Set category for sidebar links
        window.sidebar_links_category = 'pageacademics';

        Academics.load_cards_for_viewport();
        // Set initial display state
        Academics.is_desktop = get_is_desktop();

        // Monitor for viewport changes and reorder cards if needed
        $(window).resize(function(){
            if (Academics.is_desktop !== get_is_desktop()){
                Academics.load_cards_for_viewport();
                Academics.is_desktop = get_is_desktop();
            }
        });
    },

    load_cards_for_viewport: function() {
        if (get_is_desktop()) {
            Academics._load_desktop_cards();
        } else {
            Academics._load_mobile_cards();
        }
    },

    body_cards: function() {
        return [
            OutageCard,
            GradeCard,
            CourseCards,
            VisualScheduleCard,
            TextbookCard,
            PrevTermCourseCards,
            PrevTermCourseCards1,
            GradStatusCard,
            GradCommitteeCard,
            FutureQuarterCardA,
            FutureQuarterCard1
        ];
    },

    _load_desktop_cards: function() {
        Academics._reset_content_divs();
        var desktop_body_cards = Academics.body_cards();
        var desktop_sidebar_cards = [
            SidebarLinks
        ];

        Cards.load_cards_in_order(desktop_body_cards, $("#academics_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#academics_sidebar_cards"));
    },

    _load_mobile_cards: function() {
        Academics._reset_content_divs();
        var mobile_cards = Academics.body_cards();
        mobile_cards.push(SidebarLinks);
        Cards.load_cards_in_order(mobile_cards, $("#academics_content_cards"));
    },

    _reset_content_divs: function() {
        resetCardRenderCalled();
        $("#academics_content_cards").html('');
        $("#academics_sidebar_cards").html('');
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.Academics = Academics;
