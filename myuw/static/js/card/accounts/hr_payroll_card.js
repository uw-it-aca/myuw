var HRPayrollCard = {
    name: 'HRPayrollCard',
    dom_target: undefined,

    render_init: function() {
        var source   = $("#hr_payroll_card").html();
        var template = Handlebars.compile(source);
        var compiled = template({
            card_name: HRPayrollCard.name,
            is_seattle: (window.user.seattle || window.user.seattle_affil),
            is_bothell: (window.user.bothell || window.user.bothell_affil),
            is_tacoma: (window.user.tacoma || window.user.tacoma_affil),
            is_faculty: window.user.faculty,
            is_employee: (window.user.employee || window.user.clinician),
            is_stud_employee: window.user.stud_employee
        });

        HRPayrollCard.dom_target.html(compiled);
        LogUtils.cardLoaded(HRPayrollCard.name, HRPayrollCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.HRPayrollCard = HRPayrollCard;
