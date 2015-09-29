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
            is_faculty: user.faculty,
            show_card: user.stud_employee | user.faculty
        };
        EmpFacStudentCard.dom_target.html(template(template_data));
        LogUtils.cardLoaded(EmpFacStudentCard.name, EmpFacStudentCard.dom_target);
    }
};
