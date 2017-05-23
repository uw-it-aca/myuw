var Grades = {
    show_grades: function(term) {
        showLoading();
        WebServiceData.require({grade_data: new GradeData(term)}, Grades.render_grades);
    },

    render_grades: function(resources) {
        $('html,body').animate({scrollTop: 0}, 'fast');

        var grade_data = resources.grade_data.data;
        var source = $("#grades").html();
        var template = Handlebars.compile(source);

        $("#main-content").html(template(grade_data));
    }
};
