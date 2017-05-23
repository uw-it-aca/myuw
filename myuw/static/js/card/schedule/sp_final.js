var FinalExamCard = {
    name: 'FinalExamCard',
    dom_target: undefined,
    term: 'current',

    render_init: function(term) {
        if (!window.user.student ||
            !(window.card_display_dates.is_after_last_day_of_classes &&
              window.card_display_dates.is_before_end_of_finals_week)) {
            $("#FinalExamCard").hide();
            return;
        }

        debugger
        WebServiceData.require({course_data: new CourseData(FinalExamCard.term)},
                               FinalExamCard.render_upon_data);
    },

    render_error: function(course_resource_error) {
        if (course_resource_error) {
            // CourseCards displays the message
            $("#FinalExamCard").hide();
            return true;
        }

        return false;
    },

    render_upon_data: function(resources) {
        var course_resource = resources.course_data;

        if (FinalExamCard.render_error(course_resource.error)) {
            return;
        }

        course_resource.normalize_instructors();
        var course_data = course_resource.data;
        source = $("#final_exam_card_content").html();
        template = Handlebars.compile(source);
        FinalExamCard.dom_target.html(template(course_data));
        FinalExamSchedule.render(course_data, FinalExamCard.term, false);
        LogUtils.cardLoaded(FinalExamCard.name, FinalExamCard.dom_target);
    }

};

 
