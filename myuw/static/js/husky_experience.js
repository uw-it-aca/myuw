var HuskyExperiencePage = {
    is_desktop: undefined,

    render: function() {
        showLoading();
        HuskyExperiencePage.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var HuskyExperience_source = $("#husky_experience_page").html();
        var template = Handlebars.compile(HuskyExperience_source);

        $("#main-content").html(template());


        HuskyExperiencePage.load_cards_for_viewport();
        // Set initial display state
        HuskyExperiencePage.is_desktop = get_is_desktop();

    },

    load_cards_for_viewport: function() {
        if (get_is_desktop()) {
            HuskyExperiencePage._load_desktop_cards();
        } else {
            HuskyExperiencePage._load_mobile_cards();
        }
    },

    _load_desktop_cards: function() {
    //    HuskyExperiencePage._reset_content_divs();
        var desktop_body_cards = [
    /*        CommonProfileCard,
            DirectoryInfoCard,
            StudentInfoCard,
            ApplicantProfileCard */
        ];
        var desktop_sidebar_cards = [
        /*    ProfileHelpLinksCard */
        ];

        Cards.load_cards_in_order(desktop_body_cards, $("#huskyx_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#huskyx_sidebar_cards"));
    },

    _load_mobile_cards: function() {
    //    HuskyExperiencePage._reset_content_divs();
        var mobile_cards = [
        /*        CommonProfileCard,
            DirectoryInfoCard,
            StudentInfoCard,
            ApplicantProfileCard */
        ];
        Cards.load_cards_in_order(mobile_cards, $("#huskyx_content_cards"));
    },

    _reset_content_divs: function() {
        $("#huskyx_content_cards").html('');
        $("#huskyx_sidebar_cards").html('');
    }
};
