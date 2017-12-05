var MedicineAccountsCard = {
    name: 'MedicineAccountsCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_profile_data(MedicineAccountsCard.render_upon_data, MedicineAccountsCard.render_error);
    },


    render_upon_data: function() {
        var profile_data = WSData.profile_data();
        try {
            if(profile_data.password.has_active_med_pw) {
                MedicineAccountsCard._render();
            } else {
                remove_card(MedicineAccountsCard.dom_target);
            }
        } catch (e) {
            remove_card(MedicineAccountsCard.dom_target);
        }

    },

    render_error: function() {
        MedicineAccountsCard.dom_target.html(CardWithError.render("UW Medicine"));
        LogUtils.cardLoaded(MedicineAccountsCard.name, MedicineAccountsCard.dom_target);
    },

    _render: function() {
        var data = WSData.profile_data().password;
        var source   = $("#accounts_medicine").html();
        var template = Handlebars.compile(source);
        var raw = template(data);
        MedicineAccountsCard.dom_target.html(raw);

        LogUtils.cardLoaded(MedicineAccountsCard.name, MedicineAccountsCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.MedicineAccountsCard = MedicineAccountsCard;
