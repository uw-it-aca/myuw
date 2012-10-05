var CourseList = {
    show_list: function(course_index) {
        WSData.fetch_course_data(CourseList.render_list, [course_index]);
    },

    render_list: function(course_index) {
        if (course_index === undefined) {
            $('html,body').animate({scrollTop: 0}, 'fast');
        }

        WSData.normalize_instructors();
        var course_data = WSData.course_data();
        var index = 0;
        for (index = 0; index < course_data.sections.length; index++) {
            course_data.sections[index].index = index;
        }

        source = $("#quarter-list").html();
        template = Handlebars.compile(source);
        $("#page-header").html(template({year: course_data.year, quarter: course_data.quarter}));

        // In case someone backs onto the page from a modal
        Modal.hide();

        // Handle the case of no courses
        if (course_data.sections.length == 0) {
            var source   = $("#no-courses").html();
            var template = Handlebars.compile(source);
            $("#courselist").html(template(course_data));
            return;
        }

        var source   = $("#courses").html();
        var template = Handlebars.compile(source);
        $("#courselist").html(template(course_data));

        if (course_index !== undefined) {
            $("#course"+course_index).collapse('show');
            console.log("Scrolling to course_wrapper"+course_index);
            $('html,body').animate({scrollTop: $("#course_wrapper"+course_index).offset().top},'slow');
        }

        $(".display_visual_sched").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "visual"
            },  "", "/mobile/visual");

            return false;
        });


        $(".instructor").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "instructor",
                instructor: ev.target.rel
            },  "", "/mobile/instructor/"+ev.target.rel);

            return false;
        });


        $(".show_textbooks").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "textbooks",
            },  "", "/mobile/textbooks");

            return false;
        });


    }
};

