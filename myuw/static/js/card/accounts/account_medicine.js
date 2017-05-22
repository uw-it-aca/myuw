var MedicineAccountsCard = {
    name: 'Medicine-AccountsCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_profile_data(MedicineAccountsCard.render_upon_data, MedicineAccountsCard.render_error);
    },


    render_upon_data: function() {
        var profile_data = WSData.profile_data();
        if(profile_data.password.has_active_med_pw) {
            MedicineAccountsCard._render();
        } else {
            MedicineAccountsCard.dom_target.hide();
        }
    },

    render_error: function() {
        MedicineAccountsCard.dom_target.html(CardWithError.render("UW Medicine"));
        LogUtils.cardLoaded(MedicineAccountsCard.name, MedicineAccountsCard.dom_target);
    },

    _render: function() {
        var source   = $("#accounts_medicine").html();
        var template = Handlebars.compile(source);
        var compiled = template(WSData.profile_data().password);
        MedicineAccountsCard.dom_target.html(compiled);
        LogUtils.cardLoaded(MedicineAccountsCard.name, MedicineAccountsCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.MedicineAccountsCard = MedicineAccountsCard;
