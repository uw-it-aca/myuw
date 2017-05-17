var HRPayrollCard = {
    name: 'HRPayrollCard',
    dom_target: undefined,

    render_init: function() {
        if (!(window.user.employee || window.user.faculty || window.user.stud_employee)) {
            $("#HRPayrollCard").hide();
            return;
        }

        HRPayrollCard._render();
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
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.HRPayrollCard = HRPayrollCard;
