var VisualSchedule = {
    show_visual_schedule: function() {
        WSData.fetch_course_data(VisualSchedule.render);
    },

    render: function() {
        var source   = $("#visual_schedule").html();
        var template = Handlebars.compile(source);

        var course_data = WSData.course_data();
        $("#courselist").html(template(course_data));

        source = $("#quarter-visual").html();
        template = Handlebars.compile(source);
        $("#quarter-info").html(template({year: course_data.year, quarter: course_data.quarter}));

        $(".display_list_sched").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "course_list",
            },  "", "/my/");
        });


        $(".instructor").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "instructor",
                instructor: ev.target.rel
            },  "", "/my/instructor/"+ev.target.rel);
        });

    }
};
