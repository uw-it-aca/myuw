var RenderPage = function () {
    CommonLoading.render_init();
    $("#app_navigation").show();
    Cards.load_cards_in_order([ProfileCard], $("#profile_content"));
};