var VisualScheduleCard = {
    name: 'VisualScheduleCard',
    dom_target: undefined,
    term: 'current',
    ck_student_schedule: false,
    ck_instructor_schedule: false,

    hide_card: function() {
        if (window.user.student) {
            VisualScheduleCard.ck_student_schedule = true;
        }
        if (window.user.instructor) {
            VisualScheduleCard.ck_instructor_schedule = true;
        }
        if (VisualScheduleCard.ck_student_schedule || VisualScheduleCard.ck_instructor_schedule) {
            return false;
        }
        return true;
    },

    render_init: function(term, course_index) {
        console.log('INIT');
        if (VisualScheduleCard.hide_card()) {
            $("#VisualScheduleCard").hide();
            return;
        }
        console.log('123');
        WSData.fetch_visual_schedule_term(VisualScheduleCard.term,
                                          VisualScheduleCard.render_handler,
                                          VisualScheduleCard.render_handler);
    },

    render_handler: function() {
        console.log('handle');
    },

    _render_error: function() {
        console.log('err');
        $("#VisualScheduleCard").hide();
    },

    // The course_index will be given when a modal is shown.
    _render: function() {
    },

};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.VisualScheduleCard = VisualScheduleCard;
