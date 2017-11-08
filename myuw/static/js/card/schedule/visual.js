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
        console.log(VisualScheduleCard.term);
        WSData.fetch_visual_schedule_term(VisualScheduleCard.term,
                                          VisualScheduleCard.render_handler,
                                          VisualScheduleCard.render_handler);
    },

    render_handler: function() {
        var cur = WSData.visual_schedule_data('current');
        var period = cur[0];
        period.total_sections = true;
        period.quarter = "foo";
        period.year = 2012 ;
        console.log('render handle');
        console.log(period);
        console.log();
        source = $("#visual_schedule_card_content").html();
        template = Handlebars.compile(source);
        t = template(period);
        VisualScheduleCard.dom_target.html(t);
        console.log(t);
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
