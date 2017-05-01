var RenderPage = function () {
    CommonLoading.render_init();
    $("#app_navigation").show();
    Cards.load_cards_in_order([AccountsCard, MedicineAccountsCard], $("#account_card_content"));
};