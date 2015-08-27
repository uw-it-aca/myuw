var Grades = {
    show_grades: function(term) {
        showLoading();
        WSData.fetch_grades_for_term(term, Grades.render_grades, [term]);
    },

    render_grades: function(term) {
        $('html,body').animate({scrollTop: 0}, 'fast');

        var grade_data = WSData.grade_data_for_term(term);
        var source = $("#grades").html();
        var template = Handlebars.compile(source);

        $("#main-content").html(template(grade_data));
    }
};
