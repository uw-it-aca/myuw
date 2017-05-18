var RenderPage = function () {
    CommonLoading.render_init();
    $("#app_navigation").show();
    WSData.fetch_profile_data(RenderAfterAjax, RenderAfterAjaxError);

};

var RenderAfterAjax = function () {
    var profile_data = WSData.profile_data();
    _render_cards(profile_data.password.has_active_med_pw);

};

var RenderAfterAjaxError = function () {
    _render_cards(false);
};

var _render_cards = function(has_medicine) {
    // will ultimately have more than acct and med acct cards here
    var card_order = [
        AccountsCard,
        HRPayrollCard];

    if(has_medicine){
        card_order.unshift(MedicineAccountsCard);
    }

    Cards.load_cards_in_order(card_order, $("#account_card_content"));
};
