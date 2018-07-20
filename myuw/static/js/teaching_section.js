var TeachingSection = {
    is_desktop: undefined,

    render: function() {
        showLoading();
        TeachingSection.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var teaching_source = $("#teaching_section").html();
        var template = Handlebars.compile(teaching_source);

        $("#main-content").html(template({
            'seattle_affil': window.user.seattle_emp,
            'bothell_affil': window.user.bothell_emp,
            'tacoma_affil': window.user.tacoma_emp
        }));

        TeachingSection.load_cards_for_viewport();
        // Set initial display state
        TeachingSection.is_desktop = get_is_desktop();

        // Monitor for viewport changes and reorder cards if needed
        $(window).resize(function(){
            if (TeachingSection.is_desktop !== get_is_desktop()){
                TeachingSection.load_cards_for_viewport();
                TeachingSection.is_desktop = get_is_desktop();
            }
        });
    },

    load_cards_for_viewport: function() {
        if (get_is_desktop()) {
            TeachingSection._load_desktop_cards();
        } else {
            TeachingSection._load_mobile_cards();
        }
    },

    _load_desktop_cards: function() {
        TeachingSection._reset_content_divs();
        var desktop_body_cards = [
            InstructorSectionCard
        ];
        var desktop_sidebar_cards = [
            TeachingResourcesCard
        ];
        Cards.load_cards_in_order(desktop_body_cards, $("#teaching_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#teaching_accounts_cards"));
    },

    _load_mobile_cards: function() {
        TeachingSection._reset_content_divs();
        var mobile_cards = [
            InstructorSectionCard,
            TeachingResourcesCard
        ];
        Cards.load_cards_in_order(mobile_cards, $("#teaching_content_cards"));
    },

    _reset_content_divs: function() {
        $("#teaching_content_cards").html('');
        $("#teaching_accounts_cards").html('');
    }
};
