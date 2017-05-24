var ProfilePage = {
    is_desktop: undefined,

    render: function() {
        showLoading();
        CommonLoading.render_init();
        ProfilePage.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var profile_source = $("#profile_page").html();
        var template = Handlebars.compile(profile_source);

        $("#main-content").html(template());

        ProfilePage.load_cards_for_viewport();
        // Set initial display state
        ProfilePage.is_desktop = get_is_desktop();

        // Monitor for viewport changes and reorder cards if needed
        $(window).resize(function(){
            if (ProfilePage.is_desktop !== get_is_desktop()){
                ProfilePage.load_cards_for_viewport();
                ProfilePage.is_desktop = get_is_desktop();
            }
        });
    },

    load_cards_for_viewport: function() {
        if (get_is_desktop()) {
            ProfilePage._load_desktop_cards();
        } else {
            ProfilePage._load_mobile_cards();
        }
    },

    _load_desktop_cards: function() {
        ProfilePage._reset_content_divs();
        var desktop_body_cards = [
            CommonProfileCard,
            DirectoryInfoCard
        ];
        var desktop_sidebar_cards = [
            ProfileHelpLinksCard
        ];

        Cards.load_cards_in_order(desktop_body_cards, $("#profile_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#profile_sidebar_cards"));
    },

    _load_mobile_cards: function() {
        ProfilePage._reset_content_divs();
        var mobile_cards = [
            CommonProfileCard,
            DirectoryInfoCard
        ];
        Cards.load_cards_in_order(mobile_cards, $("#profile_content_cards"));
    },

    _reset_content_divs: function() {
        $("#profile_content_cards").html('');
        $("#profile_sidebar_cards").html('');
        $("#calendar_banner_location_desktop").html('');
        $("#calendar_banner_location_mobile").html('');
    }
};
