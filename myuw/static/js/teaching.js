var Teaching = {
    is_desktop: undefined,

    render: function() {
        showLoading();
        Teaching.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var teaching_source = $("#teaching").html();
        var template = Handlebars.compile(teaching_source);

        $("#main-content").html(template({
            'seattle_affil': window.user.seattle_emp,
            'bothell_affil': window.user.bothell_emp,
            'tacoma_affil': window.user.tacoma_emp
        }));

        Teaching.load_cards_for_viewport();
        // Set initial display state
        Teaching.is_desktop = get_is_desktop();

        // Monitor for viewport changes and reorder cards if needed
        $(window).resize(function(){
            if (Teaching.is_desktop !== get_is_desktop()){
                Teaching.load_cards_for_viewport();
                Teaching.is_desktop = get_is_desktop();
            }
        });
    },

    load_cards_for_viewport: function() {
        if (get_is_desktop()) {
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
            TeachingResourcesCard
        ];
        Cards.load_cards_in_order(desktop_body_cards, $("#teaching_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#teaching_accounts_cards"));
    },

    _load_mobile_cards: function() {
        Teaching._reset_content_divs();
        var mobile_cards = [
            InstructorCourseCards,
            TeachingResourcesCard
        ];
        Cards.load_cards_in_order(mobile_cards, $("#teaching_content_cards"));
    },

    _reset_content_divs: function() {
        $("#teaching_content_cards").html('');
        $("#teaching_accounts_cards").html('');
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.Teaching = Teaching;
