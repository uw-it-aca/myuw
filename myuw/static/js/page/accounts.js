var RenderPage = function () {
    CommonLoading.render_init();
    $("#app_navigation").show();
    Cards.load_cards_in_order([MedicineAccountsCard, AccountsCard], $("#account_card_content"));
};