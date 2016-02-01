var CourseSchePanel = {

    render: function (c_section) {

        var source = $("#course_sche_panel").html();
        var template = Handlebars.compile(source);
        $('#eval-course-sche' + c_section.index).html(template(c_section));
    }
};

 
