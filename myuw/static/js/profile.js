var ProfilePage = {
    is_desktop: undefined,

    render: function() {
        showLoading();
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
        ProfilePage._load_cards();
    },

    _load_cards: function() {
        ProfilePage._reset_content_divs();
        var body_cards = [
            CommonProfileCard,
            EmployeeInfoCard,
            StudentInfoCard,
            ApplicantProfileCard
        ];
        var sidebar_cards = [
            ProfileHelpLinksCard
        ];

        Cards.load_cards_in_order(body_cards, $("#profile_content_cards"));
        Cards.load_cards_in_order(sidebar_cards, $("#profile_sidebar_cards"));
    },


    _reset_content_divs: function() {
        $("#profile_content_cards").html('');
        $("#profile_sidebar_cards").html('');
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.ProfilePage = ProfilePage;
