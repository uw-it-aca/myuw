var RenderPage = function () {
    CommonLoading.render_init();
    Cards.load_cards_in_order([aAccountsCard], $("#account_card_content"));
};