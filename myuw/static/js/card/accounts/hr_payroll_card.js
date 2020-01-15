var HRPayrollCard = {
    name: 'HRPayrollCard',
    dom_target: undefined,

    render_init: function() {
        Handlebars.registerPartial('workday_link', $("#workday_link").html());
        var source   = $("#hr_payroll_card").html();
        var template = Handlebars.compile(source);
        var data = {
            card_name: HRPayrollCard.name,
            is_seattle: window.user.seattle_emp,
            is_bothell: window.user.bothell_emp,
            is_tacoma: window.user.tacoma_emp,
            is_faculty: window.user.faculty,
            is_stud_employee: window.user.stud_employee,
            truncate_view: (window.user.retiree || window.user.past_employee)
            };
        var compiled = template(data);
        HRPayrollCard.dom_target.html(compiled);
        LogUtils.cardLoaded(HRPayrollCard.name, HRPayrollCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.HRPayrollCard = HRPayrollCard;
