var CourseCardContentPanel = {

    render: function (c_section, eval_data) {

        var index = c_section.index;

        // Determine if we have valid eval data for the section
        var has_valid_eval = (eval_data &&
                              eval_data.sections &&
                              eval_data.sections.length > 0 &&
                              eval_data.sections[index] &&
                              eval_data.sections[index].evaluation_data &&
                              eval_data.sections[index].evaluation_data.length > 0 ? true : false);
        c_section.has_eval = has_valid_eval;
        c_section.evals = (has_valid_eval ? eval_data.sections[index].evaluation_data : null);

        // Determine if there was an err when fetching the section eval data
        var eval_data_err = (eval_data &&
                             !has_valid_eval &&
                             eval_data.sections[index].evaluation_data === null ? true :false);
        c_section.eval_data_err = eval_data_err;

        var source = $("#course_card_content_panel").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#course_card_content' + index).html(raw);

        if (has_valid_eval) {
            CourseEvalPanel.render(c_section);
        }

        CourseSchePanel.render(c_section);

        CourseResourcePanel.render(c_section);

        if (c_section.instructors) {
            CourseInstructorPanel.render(c_section);
        }
    }
};
