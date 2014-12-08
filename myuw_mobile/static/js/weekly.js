var Weekly = {
    show_current_week: function() {
        showLoading();
        WSData.fetch_current_week_data(Weekly.render_week);
    },

    render_week: function(data) {

        var current_week = data.current_week,
            template, source;

        if (current_week > 0 && current_week < 11) {
            var name = "#week"+current_week+"_outline";

            if ($(name).length) {
                source = $(name).html();
                template = Handlebars.compile(source);
            }
        }

        if (!template) {
            source = $("#week_other_outline").html();
            template = Handlebars.compile(source);
        }

        var visual_schedule = VisualSchedule.get_html(data.schedule);

        var course_list = CourseListCard.render_card(data.schedule, current_week);

        $("#main-content").html(template({
            visual_schedule: visual_schedule,
            course_list: course_list
        }));
        CourseListCard.init_events();
    }
};
