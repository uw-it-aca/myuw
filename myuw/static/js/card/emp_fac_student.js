var EmpFacStudentCard = {
    name: 'EmpFacStudentCard',
    dom_target: undefined,

    render_init: function() {
        EmpFacStudentCard._render();
    },

    _render: function () {
        var source = $("#student_empfac_card_content").html();
        var template = Handlebars.compile(source);
        var template_data;
        template_data = {
            is_student_employee: user.stud_employee,
            is_employee: user.employee,
            show_card: user.employee
        };
        EmpFacStudentCard.dom_target.html(template(template_data));
        LogUtils.cardLoaded(EmpFacStudentCard.name, EmpFacStudentCard.dom_target);
    }
};
