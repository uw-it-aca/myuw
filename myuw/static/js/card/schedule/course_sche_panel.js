var CourseSchePanel = {

    render: function (c_section) {
        if (c_section.class_website_url || c_section.lib_subj_guide || c_section.canvas_url) {
            c_section.has_resources = true;
        }

        var source = $("#course_sche_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#eval-course-sche' + c_section.index).html(raw);
    }
};

 
