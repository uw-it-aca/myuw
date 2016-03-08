var CourseSchePanel = {

    render: function (c_section) {
        var source = $("#course_sche_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#sche_on_course_card' + c_section.index).html(raw);
    }
};
