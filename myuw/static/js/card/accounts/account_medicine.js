var MedicineAccountsCard = {
    name: 'Medicine--AccountsCard',
    dom_target: undefined,

    render_init: function() {
        WebServiceData.require({profile_data: new ProfileData()},
                               MedicineAccountsCard.render_upon_data);
    },


    render_upon_data: function(resources) {
        var profile_resource = resources.profile_data;

        if (MedicineAccountsCard.render_error(profile_resource.error)) {
            return;
        }

        var profile_data = profile_resource.data;
        if(profile_data.password.has_active_med_pw) {
            MedicineAccountsCard._render(profile_data);
        } else {
            MedicineAccountsCard.dom_target.hide();
        }
    },

    render_error: function(profile_resource_error) {
        if (profile_resource_error) {
            MedicineAccountsCard.dom_target.html(CardWithError.render("UW Medicine"));
            LogUtils.cardLoaded(MedicineAccountsCard.name, MedicineAccountsCard.dom_target);
            return true;
        }

        return false;
    },

    _render: function(profile_data) {
        var source   = $("#accounts_medicine").html();
        var template = Handlebars.compile(source);
        var compiled = template(profile_data.password);
        MedicineAccountsCard.dom_target.html(compiled);
        LogUtils.cardLoaded(MedicineAccountsCard.name, MedicineAccountsCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.MedicineAccountsCard = MedicineAccountsCard;
