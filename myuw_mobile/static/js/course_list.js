var CourseList = {
    show_list: function(course_index) {
        WSData.fetch_course_data(CourseList.render_list, [course_index]);
    },

    render_list: function(course_index) {
        if (course_index === undefined) {
            $('html,body').animate({scrollTop: 0}, 'fast');
        }
        var source   = $("#courses").html();
        var template = Handlebars.compile(source);

        WSData.normalize_instructors();
        var course_data = WSData.course_data();
        var index = 0;
        for (index = 0; index < course_data.sections.length; index++) {
            course_data.sections[index].index = index;
        }

        $("#courselist").html(template(course_data));

        source = $("#quarter-list").html();
        template = Handlebars.compile(source);
        $("#quarter-info").html(template({year: course_data.year, quarter: course_data.quarter}));

        if (course_index !== undefined) {
            $("#course"+course_index).collapse('show');
            $('html,body').animate({scrollTop: $("#course_wrapper"+course_index).offset().top},'slow');
        }

        $(".display_visual_sched").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "visual",
            },  "", "/my/visual");

            return false;
        });


        $(".instructor").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "instructor",
                instructor: ev.target.rel
            },  "", "/my/instructor/"+ev.target.rel);

            return false;
        });


    }
};

