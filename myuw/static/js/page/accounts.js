var RenderPage = function () {
    CommonLoading.render_init();
    $("#app_navigation").show();
    WebServiceData.require({profile_data: new ProfileData()},
                           RenderAfterAjax);
    }
};

var RenderAfterAjax = function (resources) {
    var profile_resource = resources.profile_data;

    if (RenderAfterAjaxError(profile_resource.error)) {
        return;
    }

    var profile_data = profile_resource.data;
    _render_cards(profile_data.password.has_active_med_pw);

};

var RenderAfterAjaxError = function (profile_resource_error) {
    if (profile_resource_error) {
        _render_cards(false);
        return true;
    }

    return false;
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
