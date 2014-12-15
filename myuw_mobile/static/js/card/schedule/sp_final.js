var FinalExamCard = {
    name: 'FinalExamCard',
    dom_target: undefined,
    term: 'current',

    render_init: function(term, course_index) {
        if (window.card_display_dates.is_after_last_day_of_classes &&
            window.card_display_dates.is_before_end_of_finals_week) {
            WSData.fetch_current_course_data(FinalExamCard.render_upon_data, FinalExamCard.render_error);
        }
        else {
            $("#FinalExamCard").hide();
        }
    },

    _has_all_data: function () {
        if (WSData.normalized_course_data(FinalExamCard.term)) {
            return true;
        }
        return false;
    },

    render_error: function() {
        FinalExamCard.dom_target.html(CardWithNoCourse.render(titilizeTerm(FinalExamCard.term)));
    },

    render_upon_data: function(course_index) {
        if (!FinalExamCard._has_all_data()) {
            return;
        }
        var course_data = WSData.normalized_course_data(FinalExamCard.term);
        source = $("#final_exam_card_content").html();
        template = Handlebars.compile(source);
        FinalExamCard.dom_target.html(template(course_data));
        FinalExamSchedule.render(course_data, FinalExamCard.term, false);
    }

};

 
