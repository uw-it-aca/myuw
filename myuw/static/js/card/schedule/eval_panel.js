var CourseEvalPanel = {

    render: function (c_section, fetched_eval) {

        var eval_data = (fetched_eval? WSData.iasystem_data(): null);
        var index = c_section.index;
        
        // has valid eval data
        var has_valid_eval = (eval_data && eval_data.sections && eval_data.sections.length > 0 && eval_data.sections[index] && eval_data.sections[index].evaluation_data && eval_data.sections[index].evaluation_data.length > 0 ? true : false);
        c_section.has_eval = has_valid_eval;
        c_section.evals = (has_valid_eval ? eval_data.sections[index].evaluation_data : null);

        // failed to fetch the eval data for the section
        var eval_data_err = (!has_valid_eval &&  eval_data.sections[index].evaluation_data === null ? true :false);
        c_section.eval_data_err = eval_data_err;

        var source = $("#course_eval_panel").html();
        var template = Handlebars.compile(source);
        $('#course-eval' + index).html(template(c_section));

        CourseSchePanel.render(c_section);

        if (c_section.class_website_url || c_section.lib_subj_guide || c_section.canvas_url) {
            c_section.has_resources = true;
        }
        CourseResourcePanel.render(c_section);

        CourseInstructorPanel.render(c_section);
    }
};

 
