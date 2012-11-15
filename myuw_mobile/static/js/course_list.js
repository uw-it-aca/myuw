var CourseList = {
    show_list: function(course_index) {
        showLoading();
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
            if (course_data.sections[index].class_website_url || course_data.sections[index].canvas_url) {
                course_data.sections[index].has_resources = true;
            }
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

        $(".accordion-body").on('shown', function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("expand_course_"+course_id);
        });

        $(".accordion-body").on('hidden', function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("collapse_course_"+course_id);
        });

        $(".course_website").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id);
        });

        $(".course_canvas_site").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_canvas_website_"+course_id);
        });

        $(".show_map").on("click", function(ev) {
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_course_list_"+building);
        });


        $(".display_visual_sched").bind("click", function(ev) {
            WSData.log_interaction("course_list_view_visual_schedule");

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

