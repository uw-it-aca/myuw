var AccountsPage = {
    is_desktop: undefined,

    render: function() {
        showLoading();
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
            AccountsPage.order_card_list(get_is_desktop());
        });
    },

    load_cards_for_viewport: function() {
        AccountsPage._load_cards();
    },

    _load_cards: function(){
        var cards = AccountsPage._get_card_order_by_affiliation();
        if(cards){
            Cards.load_cards_in_order(cards, $("#accounts_content_cards"));
            AccountsPage.order_card_list(get_is_desktop());
        }
        $(window).on("card-hide", function(ev) {
            AccountsPage.order_card_list(get_is_desktop());
        });
    },

    order_card_list: function(is_desktop){
        var left_list_elem = $("#accounts_content_cards"),
            right_list_elem = $("#accounts_sidebar_cards"),
            all_cards = left_list_elem.children().add(right_list_elem.children()),
            left_list = [],
            right_list = [];

        var sorted_cards = all_cards.sort(AccountsPage._sort_cards);
        if(is_desktop){
            for(var i=0; i<sorted_cards.length; i++){
                if(i%2 === 0){
                    left_list.push(sorted_cards[i]);
                } else {
                    right_list.push(sorted_cards[i]);
                }
            }
            left_list_elem.html(left_list);
            right_list_elem.html(right_list);
        } else {
            left_list_elem.html(sorted_cards);
        }
    },

    _sort_cards: function(a, b){
        var order_a = parseInt($(a).attr('data-order'));
        var order_b = parseInt($(b).attr('data-order'));
        return (order_a < order_b) ? -1 : (order_a > order_b) ? 1 : 0;
    },

    _get_card_order_by_affiliation: function(){
        // affiliation precedence: student>employee
        var cards = [];
        if(window.user.student) {
            cards.push(TuitionCard);
        }

        cards.push(MedicineAccountsCard);

        if(window.user.student || window.user.past_stud ||
           window.user.employee || window.user.past_employee) {
            cards.push(HuskyCard);
        }

        if((window.user.undergrad || window.user.grad) &&
           window.user.seattle) {
            cards.push(HfsSeaCard);
        }

        if(window.user.stud_employee ||
           window.user.instructor) {
            cards.push(HRPayrollCard);
        }

        cards.push(LibraryCard);

        if(window.user.student ||
           window.user.employee) {
            cards.push(UPassCard);
        }

        cards.push(UwnetidCard);
        return cards;
    },

    _reset_content_divs: function() {
        $("#accounts_content_cards").html('');
        $("#accounts_sidebar_cards").html('');
    }

};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.AccountsPage = AccountsPage;
