var AccountsPage = {
    is_desktop: undefined,

    render: function() {
        showLoading();
        CommonLoading.render_init();
        AccountsPage.make_html();
    },

    make_html: function () {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var accounts_source = $("#accounts_page").html();
        var template = Handlebars.compile(accounts_source);

        $("#main-content").html(template());

        AccountsPage.load_cards_for_viewport();
        // Set initial display state
        AccountsPage.is_desktop = get_is_desktop();

        // Monitor for viewport changes and reorder cards if needed
        $(window).resize(function(){
            if (AccountsPage.is_desktop !== get_is_desktop()){
                AccountsPage.load_cards_for_viewport();
                AccountsPage.is_desktop = get_is_desktop();
            }
        });
    },

    load_cards_for_viewport: function() {
        if (get_is_desktop()) {
            AccountsPage._load_desktop_cards();
        } else {
            AccountsPage._load_mobile_cards();
        }
    },

    _load_desktop_cards: function() {
        AccountsPage._reset_content_divs();
        var desktop_body_cards = [
            MedicineAccountsCard,
            AccountsCard,
            HRPayrollCard
        ];
        var desktop_sidebar_cards = [];

        Cards.load_cards_in_order(desktop_body_cards, $("#accounts_content_cards"));
        Cards.load_cards_in_order(desktop_sidebar_cards, $("#accounts_sidebar_cards"));
    },

    _load_mobile_cards: function() {
        AccountsPage._reset_content_divs();
        var mobile_cards = [
            MedicineAccountsCard,
            AccountsCard,
            HRPayrollCard
        ];
        Cards.load_cards_in_order(mobile_cards, $("#accounts_content_cards"));
    },

    _reset_content_divs: function() {
        $("#accounts_content_cards").html('');
        $("#accounts_sidebar_cards").html('');
        $("#calendar_banner_location_desktop").html('');
        $("#calendar_banner_location_mobile").html('');
    }

};
