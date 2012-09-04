var CourseList = {
    show_list: function() {
        WSData.fetch_course_data(CourseList.render_list);
    },

    render_list: function() {
        var source   = $("#courses").html();
        var template = Handlebars.compile(source);

        var course_data = WSData.course_data();
        $("#courselist").html(template(course_data));

        source = $("#quarter-list").html();
        template = Handlebars.compile(source);
        $("#quarter-info").html(template({year: course_data.year, quarter: course_data.quarter}));

        $(".display_visual_sched").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "visual",
            },  "", "/my/visual");
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

