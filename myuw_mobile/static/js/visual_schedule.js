var VisualSchedule = {
    show_visual_schedule: function() {
        WSData.fetch_course_data(VisualSchedule.render);
    },

    render: function() {
        alert("Show visual schedule");
    }
};
