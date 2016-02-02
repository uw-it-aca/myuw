var CourseEvalPanel = {

    render: function (c_section) {
        var source = $("#course_eval_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#course_eval' + c_section.index).html(raw);
    }
};
