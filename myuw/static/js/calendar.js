var Calendar = {
    is_desktop: undefined,

    render: function() {
        showLoading();
        Calendar.make_html();
    },

    make_html: function () {

        $('html,body').animate({scrollTop: 0}, 'fast');
        var source = $("#calendar_page").html();
        var template = Handlebars.compile(source);
        $("#main-content").html(template());

        // Set category for sidebar links
        window.sidebar_links_category = 'pagecalendar';

        Calendar.load_cards_for_viewport();
        // Set initial display state
        Calendar.is_desktop = get_is_desktop();

        // Monitor for viewport changes and reorder cards if needed
        $(window).resize(function(){
            if (Calendar.is_desktop !== get_is_desktop()){
                Calendar.load_cards_for_viewport();
                Calendar.is_desktop = get_is_desktop();
            }
        });
    },

    load_cards_for_viewport: function() {
        if (get_is_desktop()) {
            Calendar._load_desktop_cards();
        } else {
            Calendar._load_mobile_cards();
        }
    },

    _load_desktop_cards: function() {
        Calendar._reset_content_divs();
        var desktop_body_cards = [
            AcademicCalendarCard
        ];
        var desktop_sidebar_cards = [
            SidebarLinks
        ];

        Cards.load_cards_in_order(desktop_body_cards, $("#calendar_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#calendar_sidebar_cards"));
    },

    _load_mobile_cards: function() {
        Calendar._reset_content_divs();
        var mobile_cards = [
            AcademicCalendarCard,
            SidebarLinks
        ];
        Cards.load_cards_in_order(mobile_cards, $("#calendar_content_cards"));
    },

    _reset_content_divs: function() {
        resetCardRenderCalled();
        $("#calendar_content_cards").html('');
        $("#calendar_sidebar_cards").html('');
    }
};
