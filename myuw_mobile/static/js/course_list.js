var CourseList = {
    show_list: function(term, course_index) {
        showLoading();
    if (term) {
            WSData.fetch_course_data_for_term(term, CourseList.render_list, [term, course_index]);
    } else {
            WSData.fetch_course_data(CourseList.render_list, [term, course_index]);
    }
    },

    render_list: function(term, course_index) {
    var course_data;
    if (term) {
            course_data = WSData.course_data_for_term(term);
            WSData.normalize_instructors_for_term(term);
        }
        else {
            course_data = WSData.current_course_data();
            WSData.normalize_instructors_for_current_term();
        }

        if (course_index === undefined) {
            $('html,body').animate({scrollTop: 0}, 'fast');
        }

        var index = 0;
        for (index = 0; index < course_data.sections.length; index++) {
            course_data.sections[index].index = index;
            if (course_data.sections[index].class_website_url || course_data.sections[index].canvas_url) {
                course_data.sections[index].has_resources = true;
            }
        }
    
        var source = $("#quarter-header").html();
        var template = Handlebars.compile(source);
        $("#page-header").html(template({
            year: course_data.year, 
            quarter: course_data.quarter,
            summer_term: course_data.summer_term,
            page: "Courses",
        go_back_path: "",
            show_visual_button: term ? false :true,
            show_list_button: false,
            is_future_quarter: term ? true :false
        }));

        // In case someone backs onto the page from a modal
        Modal.hide();

        //console.log(course_data.sections.length)
        // Handle the case of no courses
        if (course_data.sections.length == 0) {
            $("#courselist").no_courses({
        show_future_link: term ? false : true
        });
            return;
        }

        source = $("#courses").html();
        template = Handlebars.compile(source);
        $("#courselist").html(template(course_data));
        $("#addi_links").addi_course_links({
        show_future_link: term ? false : true,
        term: term
    });

        if (course_index !== undefined) {
            $("#course"+course_index).collapse('show');
            console.log("Scrolling to course_wrapper"+course_index);
            $('html,body').animate({scrollTop: $("#course_wrapper"+course_index).offset().top},'slow');
        }

        var logging_term = term.replace(/[^a-z0-9]/gi, '_');
        var course_id = ev.currentTarget.getAttribute("rel");
        course_id = course_id.replace(/[^a-z0-9]/gi, '_');

        $(".accordion-body").on('shown', function(ev) {
        if (term) {
        WSData.log_interaction("expand_course_"+course_id+"_term_"+logging_term);
        } 
        else {
        WSData.log_interaction("expand_course_"+course_id);
        }
        });

        $(".accordion-body").on('hidden', function(ev) {
        if (term) {
        WSData.log_interaction("collapse_course_"+course_id+"_term_"+logging_term);
        }
        else {
        WSData.log_interaction("collapse_course_"+course_id);
        }
        });

        $(".course_website").on("click", function(ev) {
        if (term) {
        WSData.log_interaction("open_course_website_"+course_id+"_term_"+logging_term);
        }
        else {
        WSData.log_interaction("open_course_website_"+course_id);
        }
        });

        $(".course_canvas_site").on("click", function(ev) {
        if (term) {
        WSData.log_interaction("open_course_canvas_website_"+course_id+"_term_"+logging_term);
        }
        else {
        WSData.log_interaction("open_course_canvas_website_"+course_id);
        }
        });

        $(".show_map").on("click", function(ev) {
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
        if (term) {
        WSData.log_interaction("show_map_from_course_list_"+building+"_term_"+logging_term);
        }
        else {
        WSData.log_interaction("show_map_from_course_list_"+building);
        }
        });


        $(".instructor").on("click", function(ev) {
            var hist = window.History;
        if (term) {
        hist.pushState({
                    state: "instructor",
                    instructor: ev.target.rel,
            term: term
        },  "", "/mobile/instructor/"+term+"/"+ev.target.rel);
        }
            else {
        hist.pushState({
                    state: "instructor",
                    instructor: ev.target.rel
        },  "", "/mobile/instructor/"+ev.target.rel);
        }
        return false;
        });

        if (term) {
            $(".back_to_current").on("click", function(ev) {
                WSData.log_interaction("course_list_back_to_current");
                var hist = window.History;
                hist.replaceState({
                    state: "course_list"
                },  "", "/mobile/");
                return false;
            });
    }
        else {
            $(".display_visual_sched").bind("click", function(ev) {
            var hist = window.History;
                WSData.log_interaction("course_list_view_visual_schedule");
                hist.pushState({
                    state: "visual"
                },  "", "/mobile/visual");
        return false;
            });
        }
    }
};

