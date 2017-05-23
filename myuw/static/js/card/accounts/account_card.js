var AccountsCard = {
    name: 'AccountsCard',
    dom_target: undefined,

    render_init: function() {
        WebServiceData.require({profile_data: new ProfileData()}, 
                               AccountsCard.render);
    },

    render_error: function(profile_resource_error) {
        if (profile_resource_error) {
            AccountsCard.dom_target.html(CardWithError.render("UW NetID"));
            return true;
        }

        return false;
    },

    render: function(resources) {
        var profile_resource = resources.profile_data;

        if (AccountsCard.render_error(profile_resource.error)) {
            return;
        }

        var profile_data = profile_resource.data;
        var source   = $("#accounts_card").html();
        var template = Handlebars.compile(source);
        var compiled = template(profile_data.password);
        AccountsCard.dom_target.html(compiled);
        LogUtils.cardLoaded(AccountsCard.name, AccountsCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.AccountsCard = AccountsCard;
