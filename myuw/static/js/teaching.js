var Teaching = {
    is_desktop: undefined,

    render: function() {
        showLoading();
        CommonLoading.render_init();
        Teaching.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var teaching_source = $("#teaching").html();
        var template = Handlebars.compile(teaching_source);

        $("#main-content").html(template());

        NoticeBanner.render_init($("#notice_banner_location"));

        Teaching.load_cards_for_viewport();
        // Set initial display state
        Teaching.is_desktop = Teaching.get_is_desktop();

        // Monitor for viewport changes and reorder cards if needed
        $(window).resize(function(){
            if (Teaching.is_desktop !== Teaching.get_is_desktop()){
                Teaching.load_cards_for_viewport();
                Teaching.is_desktop = Teaching.get_is_desktop();
            }
        });
    },

    get_is_desktop: function() {
        var mobile_cutoff_width = 992;
        var viewport_width = $(window).width();
        if (viewport_width >= mobile_cutoff_width) {
            return true;
        } else {
            return false;
        }

    },

    load_cards_for_viewport: function() {
        if (Teaching.get_is_desktop()) {
            Teaching._load_desktop_cards();
        } else {
            Teaching._load_mobile_cards();
        }
    },

    _load_desktop_cards: function() {
        Teaching._reset_content_divs();
        var desktop_body_cards = [
            InstructorCourseCards
        ];
        var desktop_sidebar_cards = [
            EventsCard
        ];
        Cards.load_cards_in_order(desktop_body_cards, $("#teaching_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#teaching_accounts_cards"));
        CalendarBanner.render_init($("#calendar_banner_location_desktop"));
    },

    _load_mobile_cards: function() {
        Teaching._reset_content_divs();
        var mobile_cards = [
            InstructorCourseCards,
            EventsCard
        ];
        Cards.load_cards_in_order(mobile_cards, $("#teaching_content_cards"));
        CalendarBanner.render_init($("#calendar_banner_location_mobile"));
    },

    _reset_content_divs: function() {
        $("#teaching_content_cards").html('');
        $("#teaching_accounts_cards").html('');
        $("#calendar_banner_location_desktop").html('');
        $("#calendar_banner_location_mobile").html('');
    }

};
