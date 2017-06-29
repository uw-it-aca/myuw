var HRPayrollCard = {
    name: 'HRPayrollCard',
    dom_target: undefined,

    render_init: function() {
        if (myuwFeatureEnabled('workday_account_card') && (window.user.employee || window.user.faculty)) {
            HRPayrollCard._render();
        } else {
            $("#HRPayrollCard").hide();
        }
    },

    render_error: function() {
        HRPayrollCard.dom_target.html(CardWithError.render("UW NetID"));
    },

    _render: function() {
        var source   = $("#hr_payroll_card").html();
        var template = Handlebars.compile(source);
        var compiled = template({
            card_name: HRPayrollCard.name,
            is_faculty: window.user.faculty,
            is_clinician: window.user.clinician
        });

        HRPayrollCard.dom_target.html(compiled);
        LogUtils.cardLoaded(HRPayrollCard.name, HRPayrollCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.HRPayrollCard = HRPayrollCard;
