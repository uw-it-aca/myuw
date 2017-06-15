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
        AccountsPage._load_cards();
    },

    _load_cards: function(){
        var cards = AccountsPage._get_card_order_by_affiliation();
        if(cards){
            Cards.load_cards_in_order(cards, $("#accounts_content_cards"));
            AccountsPage.order_card_list();
        }
        $(window).on("card-hide", function(ev) {
            AccountsPage.order_card_list();
        });
    },

    order_card_list: function(){
        var left_list_elem = $("#accounts_content_cards"),
            right_list_elem = $("#accounts_sidebar_cards"),
            all_cards = left_list_elem.children().add(right_list_elem.children()),
            left_list = [],
            right_list = [];

        var sorted_cards = all_cards.sort(AccountsPage._sort_cards);

        for(var i=0; i<sorted_cards.length; i++){
            if(i%2 === 0){
                left_list.push(sorted_cards[i]);
            } else {
                right_list.push(sorted_cards[i]);
            }
        }
        left_list_elem.html(left_list);
        right_list_elem.html(right_list);


    },

    _sort_cards: function(a, b){
        var order_a = parseInt($(a).attr('data-order'));
        var order_b = parseInt($(b).attr('data-order'));
        return (order_a < order_b) ? -1 : (order_a > order_b) ? 1 : 0;
    },

    _get_card_order_by_affiliation: function(){
        // affiliation precedence: student>employee
        if(window.user.student) {
            return [
                TuitionCard,
                MedicineAccountsCard,
                HfsCard,
                LibraryCard,
                UPassCard,
                AccountsCard
            ];
        }
        if(window.user.employee){
            return [
                MedicineAccountsCard,
                HRPayrollCard,
                LibraryCard,
                UPassCard,
                HfsCard,
                AccountsCard
            ];
        }

    },

    _reset_content_divs: function() {
        $("#accounts_content_cards").html('');
        $("#accounts_sidebar_cards").html('');
    }

};
