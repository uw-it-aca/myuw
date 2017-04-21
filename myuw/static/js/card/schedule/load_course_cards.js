var CourseCards = {
    name: 'CourseCards',
    dom_target: undefined,
    term: 'current',

    render_init: function() {
        if (!window.user.student) {
            $("#CourseCards").hide();
            return;
        }

        WebServiceData.require({course_data: new CourseData(CourseCards.term)},
                               CourseCards.render);
    },

    render_upon_data: function() {
        if (!CourseCards._has_all_data()) {
            return;
        }
        CourseCards._render();
    },

    render_error: function(course_resource_error) {
        var error_code = course_resource_error ? course_resource_error.status : null;

        if (error_code == 410) {
            Error410.render();
            return true;
        }

        if (course_resource_error) {
            var raw = (error_code === 404 ? CardWithNoCourse.render(CourseCards.term) : CardWithError.render("Schedule & Course Info"));
            if (CourseCards.term === "current") {
                CourseCards.dom_target.html(raw);
            } else {
                $("#future_content").html(raw);
            }

            return true;
        }

        return false;
    },

    render: function (resources) {
        var term = CourseCards.term;
        var course_data_resource = resources.course_data;

        if (CourseCards.render_error(course_data_resource.error)) {
            return;
        }

        var course_data = course_data_resource.data;

        if (term === 'current' && window.card_display_dates.in_coursevel_fetch_window) {
            WebServiceData.require({'iasystem_data': new IASystemData()},
                                   LoadCourseEval.render,
                                   [course_data_resource]);
        }

        var source = $("#course_card_list").html();
        var courses_template = Handlebars.compile(source);
        var raw = courses_template(course_data);
        CourseCards.dom_target.html(raw);

        LoadCourseEval.render(course_data_resource, null);

        CourseCards.add_events(term);
        LogUtils.cardLoaded(CourseCards.name, CourseCards.dom_target);
    },

    add_events: function(term) {
        $(".course_website").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id, term);
        });

        $(".lib_subject_guide").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_lib_subject_guide_"+course_id, term);
        });

        $(".show_map").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_course_list_"+building, term);
        });

        $(".course_canvas_site").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_canvas_website_"+course_id, term);
        });

        $(".show_course_textbook").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("href");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_textbook_"+course_id, term);
        });

        $(".instructor").on("click", function(ev) {
            WSData.log_interaction("view_instructor_from_course_list", term);
            var hist = window.History;
            if (term) {
                hist.pushState({
                    state: "instructor",
                    instructor: ev.target.rel,
                    term: term
                },  "", "/instructor/"+term+"/"+ev.target.rel);
            }
            else {
                hist.pushState({
                    state: "instructor",
                    instructor: ev.target.rel
                },  "", "/instructor/"+ev.target.rel);
            }
            return false;
        });
    },
};
