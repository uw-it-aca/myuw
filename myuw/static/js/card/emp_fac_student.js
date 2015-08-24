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
        template_data = {};
        EmpFacStudentCard.dom_target.html(template(template_data));
    }
};
